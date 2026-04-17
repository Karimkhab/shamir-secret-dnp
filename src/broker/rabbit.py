import json
import logging
import pika

QUEUE_NAME = "shamir_queue"
logger = logging.getLogger(__name__)


def publish_message(message: dict) -> None:
    """Publish a JSON task message to the Shamir RabbitMQ queue."""
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    try:
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME)

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(message, ensure_ascii=False).encode("utf-8"),
        )
        logger.info(
            "Published task request_id=%s type=%s",
            message.get("request_id"),
            message.get("type"),
        )

    finally:
        connection.close()
