import pika

from services.mail_services import send_email
from services.pika_helper import ConnectionFactory

if __name__ == "__main__":
    connection = ConnectionFactory(
        pika.ConnectionParameters("localhost"),
        "email_queue",
        callback=lambda *args, **kwargs: send_email.delay(*args, **kwargs),
    )
    connection.consume()
