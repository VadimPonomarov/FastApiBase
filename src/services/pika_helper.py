import json
from typing import TYPE_CHECKING

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.spec import Basic, BasicProperties
from pydantic import BaseModel

from core.enums.pika import ExchangeType, QueueType
from services.mail_services import send_email

if TYPE_CHECKING:
    from pika.connection import ConnectionParameters


class MessageSchema(BaseModel):
    to_email: str
    subject: str
    message: str
    logo_url: str


class ConnectionFactory:
    def __init__(
        self,
        parameters: "ConnectionParameters",
        queue_name: str,
        queue_type: QueueType = QueueType.DURABLE,
        exchange_name: str = "",
        exchange_type: ExchangeType = ExchangeType.DIRECT,
    ):
        self.__connection: BlockingConnection = BlockingConnection(parameters)
        self.__queue_name: str = queue_name
        self.__queue_type: QueueType = queue_type
        self.__exchange_name: str = exchange_name
        self.__exchange_type: ExchangeType = exchange_type
        self.__channel = self.__connection.channel()
        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.queue_declare(queue=self.__queue_name)

    def get_connection(self) -> BlockingConnection:
        return self.__connection

    def publish(self, message: dict) -> None:
        with self.get_connection() as connection:
            message_json: bytes = json.dumps(message).encode("utf-8")
            self.__channel.basic_publish(
                exchange=self.__exchange_name,
                routing_key=self.__queue_name,
                body=message_json,
            )
            print(" [x] Sent email request")

    def consume(self) -> None:
        with self.get_connection() as connection:
            self.__channel.basic_consume(
                queue=self.__queue_name,
                on_message_callback=ConnectionFactory.get_callback,
            )
            print(" [*] Waiting for messages. To exit press CTRL+C")
            self.__channel.start_consuming()

    @staticmethod
    def get_callback(
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        email_data = json.loads(body)
        send_email.delay(
            email_data["to_email"],
            email_data["subject"],
            {
                "title": email_data["subject"],
                "message": email_data["message"],
                "logo_url": email_data["logo_url"],
            },
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def close(self) -> None:
        self.__connection.close()

    def __exit__(self) -> None:
        self.close()
