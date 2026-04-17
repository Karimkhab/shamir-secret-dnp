import json
import logging
import time

import pika

QUEUE_NAME = "shamir_queue"
logger = logging.getLogger(__name__)


def call_worker(message: dict, request_id: str, timeout: int = 10) -> dict:
    """Send a task to RabbitMQ and wait for the worker response."""
    response = None

    def on_response(ch, method, properties, body):
        nonlocal response

        if properties.correlation_id == request_id:
            response = json.loads(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # pika connection
    connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1"))
    try:
        # pika channel
        channel = connection.channel()

        # declare a queue
        channel.queue_declare(queue=QUEUE_NAME)

        # declare temporary reply queue
        reply_queue = channel.queue_declare(queue="", exclusive=True).method.queue
        channel.basic_consume(
            queue=reply_queue,
            on_message_callback=on_response,
            auto_ack=False,
        )

        # send msg to queue
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            properties=pika.BasicProperties(
                reply_to=reply_queue,
                correlation_id=request_id,
            ),
            body=json.dumps(message, ensure_ascii=False).encode("utf-8"),
        )

        # write log
        logger.info(
            "Published task request_id=%s type=%s",
            message.get("request_id"),
            message.get("type"),
        )

        deadline = time.monotonic() + timeout
        while response is None and time.monotonic() < deadline:
            connection.process_data_events(time_limit=0.2)

        if response is None:
            raise TimeoutError("worker response timeout")

        return response

    finally:
        # close connection
        connection.close()
