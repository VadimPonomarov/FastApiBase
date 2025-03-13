import pika

from services.mail_services import send_email
from services.pika_helper import ConnectionFactory

if __name__ == "__main__":
    connection = ConnectionFactory(
        pika.ConnectionParameters("localhost"),
        "email_queue",
        callback=lambda data: send_email(data),
    )
    connection.consume()
