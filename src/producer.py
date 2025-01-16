import uuid

import pika
from pydantic import BaseModel, ValidationError, conlist


class NumbersModel(BaseModel):
    numbers: conlist(int, min_length=1)


class RpcClient:

    def __init__(self, host="localhost"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, numbers) -> dict | None:
        try:
            validated_numbers = NumbersModel(numbers=numbers)
            print(
                f"Sending request: {validated_numbers}"
            )
        except ValidationError as e:
            return {"error": e.errors()}

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=validated_numbers.model_dump_json().encode('utf-8')  # Преобразование в байты
        )
        while self.response is None:
            self.connection.process_data_events()
        print(f"Received response: {self.response}")
        return self.response


def main():
    rpc_client = RpcClient()
    numbers = [1, 2, 3, 4, 5, 10]
    print(f"Requesting sum of {numbers}")
    response = rpc_client.call(numbers)
    print(f"Got response: {response}")


if __name__ == "__main__":
    from loguru import logger as log

    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
