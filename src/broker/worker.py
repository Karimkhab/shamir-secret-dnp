import json
import logging
import pika
from shamir.decoder import recover_secret
from shamir.encoder import split_secret

QUEUE_NAME = "shamir_queue"
logger = logging.getLogger(__name__)


def log_reason(message: str) -> str:
    """Format validation messages as single-token log values."""
    return message.replace(" ", "_")


def process_message(message: dict) -> dict:
    """Run a Shamir task received from RabbitMQ and return its result."""
    msg_type = message["type"]
    payload = message["payload"]

    # for splitting
    if msg_type == "split":
        return split_secret(
            secret=payload["secret"],
            threshold=payload["threshold"],
            total_shares=payload["total_shares"],
        )

    # for recovering
    if msg_type == "recover":
        secret = recover_secret(shares=payload["shares"])
        return {"secret": secret}

    raise ValueError(f"unknown task type: {msg_type}")


def send_response(ch, properties, response: dict) -> None:
    """Send the worker response to the request reply queue."""
    if not properties.reply_to:
        return

    ch.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id,
        ),
        body=json.dumps(response, ensure_ascii=False).encode("utf-8"),
    )


def callback(ch, method, properties, body) -> None:
    """Handle one queued Shamir task."""
    message = json.loads(body)
    request_id = message.get("request_id")
    msg_type = message.get("type")
    payload = message.get("payload", {})

    try:
        if msg_type == "split":
            logger.info(
                "request_id=%s operation=split event=worker_started threshold=%s total_shares=%s",
                request_id,
                payload.get("threshold"),
                payload.get("total_shares"),
            )
        elif msg_type == "recover":
            logger.info(
                "request_id=%s operation=recover event=worker_started shares_count=%s",
                request_id,
                len(payload.get("shares", [])),
            )
        else:
            logger.info(
                "request_id=%s operation=%s event=worker_started",
                request_id,
                msg_type,
            )

        result = process_message(message)
        response = {
            "request_id": request_id,
            "type": msg_type,
            "status": "completed",
            "result": result,
        }

        # write log
        if msg_type == "split":
            logger.info(
                "request_id=%s operation=split event=worker_finished success=true shares_count=%s",
                request_id,
                len(result.get("shares", [])),
            )
        else:
            logger.info(
                "request_id=%s operation=%s event=worker_finished success=true",
                request_id,
                msg_type,
            )

        # send msg to reply queue
        send_response(ch, properties, response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as exc:
        response = {
            "request_id": request_id,
            "type": msg_type,
            "status": "failed",
            "error": str(exc),
        }

        # write log
        if isinstance(exc, ValueError):
            logger.warning(
                "request_id=%s operation=%s event=worker_finished success=false reason=%s",
                request_id,
                msg_type,
                log_reason(str(exc)),
            )
        else:
            logger.exception(
                "request_id=%s operation=%s event=worker_finished success=false reason=%s",
                request_id,
                msg_type,
                log_reason(str(exc)),
            )

        # send msg to reply queue
        send_response(ch, properties, response)
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    """Start the RabbitMQ worker for Shamir tasks."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logging.getLogger("pika").setLevel(logging.WARNING)

    # pika connection
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    try:
        # pika channel
        channel = connection.channel()

        # declare a queue
        channel.queue_declare(queue=QUEUE_NAME)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=callback,
            auto_ack=False,
        )

        logger.info("service=worker event=started queue=%s", QUEUE_NAME)
        channel.start_consuming()

    finally:
        connection.close()


if __name__ == "__main__":
    main()
