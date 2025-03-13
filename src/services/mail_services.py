import os
from base64 import b64encode

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment, Mail

from celery_config import celery_app
from core.enums.templates import TemplatesLogosEnum
from settings.config import settings
from templates.email_enum import EmailTemplateEnum

load_dotenv()


class SendEmailParams[T](BaseModel):
    template_data: T
    from_email: str = settings.sendgrid.my_email
    to_email: str = settings.sendgrid.my_email
    subject: str = "Test Email"
    email_type: EmailTemplateEnum = EmailTemplateEnum.EMAIL_TEMPLATE_BASE
    logo_name: TemplatesLogosEnum = TemplatesLogosEnum.INDONESIAN_HALAL_LOGO


@celery_app.task(name="send_email_task")
def send_email(params: SendEmailParams) -> None:
    template_loader = FileSystemLoader(
        searchpath=settings.templates_path or "./templates"
    )
    env = Environment(loader=template_loader, autoescape=True)

    template = env.get_template(
        params.email_type.value or EmailTemplateEnum.EMAIL_TEMPLATE_BASE.value
    )
    html_content = template.render(params.template_data)

    with open(
        os.path.join(settings.media_path or "./media", params.logo_name.value),
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
        to_emails=params.to_email,
        subject=params.subject,
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
