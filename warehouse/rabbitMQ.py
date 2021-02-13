import pika
from django.conf import settings
from typing import Tuple

from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel


def start_connection() -> Tuple[BlockingConnection, BlockingChannel]:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE)
    return connection, channel


def send_message(channel: BlockingChannel, message: str) -> bool:
    try:
        channel.basic_publish(exchange='',
                              routing_key=settings.RABBITMQ_QUEUE,
                              body=bytes(message, encoding='utf-8'))
        return True
    except Exception as err:
        print(err)
        return False

