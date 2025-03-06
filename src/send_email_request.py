from pika import ConnectionParameters

from services.pika_helper import ConnectionFactory, MessageSchema


def send_email_request(email_data: MessageSchema) -> None:
    ConnectionFactory(
        parameters=ConnectionParameters("localhost"),
        queue_name="email_queue",
    ).publish(email_data.model_dump())


if __name__ == "__main__":
    send_email_request(
        MessageSchema(
            to_email="pvs.versia@gmail.com",
            subject="Test Subject",
            message="This is a test message.",
            logo_url="cid:logo",
        )
    )
