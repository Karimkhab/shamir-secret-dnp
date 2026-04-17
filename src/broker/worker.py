import json
import logging
import pika
from shamir.encoder import split_secret
from shamir.decoder import recover_secret

QUEUE_NAME = "shamir_queue"
logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    """

    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    message = json.loads(body)

    msg_type = message["type"]
    payload = message["payload"]
    request_id = message.get("request_id")

    try:
        if msg_type == "split":
            result = split_secret(
                secret=payload["secret"],
                threshold=payload["threshold"],
                total_shares=payload["total_shares"],
            )

        elif msg_type == "recover":
            result = recover_secret(
                shares=payload["shares"],
                expected_hash=payload["expected_hash"],
            )

        else:
            result = {"error": "unknown type"}

        logger.info(
            "Worker completed task request_id=%s type=%s",
            request_id,
            msg_type,
        )
        print("RESULT:", json.dumps({
            "request_id": request_id,
            "type": msg_type,
            "status": "completed",
            "resultKeys": sorted(result) if isinstance(result, dict) else None,
        }, ensure_ascii=False))

    except Exception as e:
        logger.exception(
            "Worker failed task request_id=%s type=%s",
            request_id,
            msg_type,
        )
        print("ERROR:", str(e))


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue = QUEUE_NAME)

    channel.basic_consume(
        queue = QUEUE_NAME,
        on_message_callback = callback,
        auto_ack = True
    )

    print("Worker started...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
