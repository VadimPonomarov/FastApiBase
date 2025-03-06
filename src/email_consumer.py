import pika

from services.pika_helper import ConnectionFactory

if __name__ == "__main__":
    connection = ConnectionFactory(
        pika.ConnectionParameters("localhost"), "email_queue"
    )
    connection.consume()
