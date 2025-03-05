import json
from typing import TYPE_CHECKING

import pika

if TYPE_CHECKING:
    from pika.connection import ConnectionParameters


class PikaConnection:
    def __init__(self, parameters: "ConnectionParameters", queue_name: str):
        self.__connection = pika.BlockingConnection(parameters)
        self.__que_name = queue_name

    def get_connection(self):
        return self.__connection

    def publish(self, message: dict):
        with self.get_connection() as connection:
            channel = connection.channel()
            channel.queue_declare(queue=self.__que_name)
            message_json = json.dumps(message).encode("utf-8")
            channel.basic_publish(
                exchange="", routing_key=self.__que_name, body=message_json
            )

    def close(self):
        self.__connection.close()

    def __exit__(self):
        self.close()
