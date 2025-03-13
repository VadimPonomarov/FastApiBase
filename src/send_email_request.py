from pika import ConnectionParameters

from core.schemas.email import MyTemplateData
from services.mail_services import SendEmailParams
from services.pika_helper import ConnectionFactory

if __name__ == "__main__":
    ConnectionFactory(
        parameters=ConnectionParameters("localhost"),
        queue_name="email_queue",
    ).publish(
        params=SendEmailParams(
            template_data=MyTemplateData(title="Test Email", message="Test Message"),
        ),
    )
