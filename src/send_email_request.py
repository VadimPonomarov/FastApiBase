from pika import ConnectionParameters

from core.schemas.email import MyTemplateData, SendEmailParams
from services.pika_helper import ConnectionFactory

if __name__ == "__main__":
    message = 'Thank you for joining us! Visit our website <a href="http://example.com">here</a> for more information.'
    ConnectionFactory(
        parameters=ConnectionParameters("localhost"),
        queue_name="email_queue",
    ).publish(
        params=SendEmailParams(
            template_data=MyTemplateData(
                title="Test Email", message=message, logo_url="cid:logo"
            ).model_dump(),
        ),
    )
