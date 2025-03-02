import json

import pika


def send_email_request(to_email, subject, message, logo_url):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="email_queue")

    email_data = {
        "to_email": to_email,
        "subject": subject,
        "message": message,
        "logo_url": logo_url,
    }
    message = json.dumps(email_data)

    channel.basic_publish(exchange="", routing_key="email_queue", body=message)
    print(" [x] Sent email request")

    connection.close()


if __name__ == "__main__":
    send_email_request(
        "pvs.versia@gmail.com", "Test Subject", "This is a test message.", "cid:logo"
    )
