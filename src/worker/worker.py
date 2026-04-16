import pika
import json

from shamir.encoder import split_secret
from shamir.decoder import recover_secret

QUEUE_NAME = "shamir_queue"


def callback(ch, method, properties, body):
    message = json.loads(body)

    msg_type = message["type"]
    payload = message["payload"]

    try:
        if msg_type == "split":
            result = split_secret(**payload)

        elif msg_type == "recover":
            result = recover_secret(**payload)

        else:
            result = {"error": "unknown type"}

        print("RESULT:", result)

    except Exception as e:
        print("ERROR:", str(e))


def main():
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