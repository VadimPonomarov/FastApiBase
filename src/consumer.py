import json

import pika
from pydantic import BaseModel, ValidationError, conlist


class NumbersModel(BaseModel):
    numbers: conlist(int, min_length=1)


def on_request(ch, method, props, body):
    try:
        numbers_model = NumbersModel.model_validate(json.loads(body.decode('utf-8')))  # Десериализация из байтов
        numbers = numbers_model.numbers
        print(f"Received request: {numbers}")

        # Обработка запроса: вычисление суммы чисел
        response = sum(numbers)
    except ValidationError as e:
        response = {"error": e.errors()}

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(response).encode('utf-8')  # Преобразование в байты
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='rpc_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    print("Awaiting RPC requests")
    channel.start_consuming()


if __name__ == "__main__":
    from loguru import logger as log

    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
