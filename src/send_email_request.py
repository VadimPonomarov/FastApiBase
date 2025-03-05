from pika import ConnectionParameters

from utils.pika_helper import ConnectionFactory


def send_email_request(to_email, subject, message, logo_url):
    email_data = {
        "to_email": to_email,
        "subject": subject,
        "message": message,
        "logo_url": logo_url,
    }
    ConnectionFactory(
        parameters=ConnectionParameters("localhost"),
        queue_name="email_queue",
    ).publish(email_data)


if __name__ == "__main__":
    send_email_request(
        "pvs.versia@gmail.com", "Test Subject", "This is a test message.", "cid:logo"
    )
