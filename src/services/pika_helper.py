import json
from typing import TYPE_CHECKING, Callable

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.spec import Basic

from core.enums.pika import ExchangeType, QueueType
from services.mail_services import SendEmailParams

if TYPE_CHECKING:
    from pika.connection import ConnectionParameters


class ConnectionFactory:
    def __init__(
        self,
        parameters: "ConnectionParameters",
        queue_name: str,
        queue_type: QueueType = QueueType.DURABLE,
        exchange_name: str = "",
        exchange_type: ExchangeType = ExchangeType.DIRECT,
        callback: Callable = None,
    ):
        self.__connection: BlockingConnection = BlockingConnection(parameters)
        self.__queue_name: str = queue_name
        self.__queue_type: QueueType = queue_type
        self.__exchange_name: str = exchange_name
        self.__exchange_type: ExchangeType = exchange_type
        self.__channel = self.__connection.channel()
        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.queue_declare(queue=self.__queue_name)
        self.__callback = callback

    def get_connection(self) -> BlockingConnection:
        return self.__connection

    def publish(self, params: SendEmailParams) -> None:
        with self.get_connection() as connection:
            self.__channel.basic_publish(
                exchange=self.__exchange_name,
                routing_key=self.__queue_name,
                body=params.model_dump_json().encode("utf-8"),
            )
            print(" [x] Sent email request")

    def consume(self) -> None:
        with self.get_connection() as connection:
            self.__channel.basic_consume(
                queue=self.__queue_name,
                on_message_callback=self.get_callback,
            )
            print(" [*] Waiting for messages. To exit press CTRL+C")
            self.__channel.start_consuming()

    def get_callback(
        self,
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        body = json.loads(body.decode("utf-8"))
        cb_params = SendEmailParams.model_dump(body)
        print(f" [x] Received {body}")
        self.__callback(**cb_params)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def close(self) -> None:
        self.__connection.close()

    def __exit__(self) -> None:
        self.close()
