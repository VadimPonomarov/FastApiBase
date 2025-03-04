import json
from base64 import b64encode

import pika
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment, Mail

from celery_config import celery_app
from settings.config import settings

load_dotenv()

template_loader = FileSystemLoader(searchpath="./templates")
env = Environment(loader=template_loader, autoescape=True)


@celery_app.task(name="send_email_task")
def send_email(to_email: str, subject: str, template_data: dict):
    template = env.get_template("email_template.html")
    html_content = template.render(template_data)

    with open(
        "./media/indonesian_halal_logo_2022.jpg",
        "rb",
    ) as logo_file:
        logo_data = logo_file.read()
        encoded_logo = b64encode(logo_data).decode()

    attachment = Attachment()
    attachment.file_content = encoded_logo
    attachment.file_type = "image/jpeg"
    attachment.file_name = "logo.jpg"
    attachment.disposition = "inline"
    attachment.content_id = "logo"

    message = Mail(
        from_email="pvs.versia@gmail.com",
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )
    message.add_attachment(attachment)

    try:
        sg = SendGridAPIClient(settings.sendgrid.api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))


def callback(ch, method, properties, body):
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


def consume_email_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="email_queue")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="email_queue", on_message_callback=callback)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
