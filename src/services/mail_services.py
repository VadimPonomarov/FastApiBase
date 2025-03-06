from base64 import b64encode

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment, Mail

from celery_config import celery_app
from settings.config import settings
from templates.email_enum import EmailTemplateEnum

load_dotenv()

template_loader = FileSystemLoader(searchpath="./templates")
env = Environment(loader=template_loader, autoescape=True)


class SendEmailParams(BaseModel):
    from_email: str = "pvs.versia@gmail.com"
    to_email: str = "pvs.versia@gmail.com"
    subject: str
    template_data: dict


@celery_app.task(name="send_email_task")
def send_email(params: SendEmailParams) -> None:
    template = env.get_template(EmailTemplateEnum.EMAIL_TEMPLATE_BASE.value)
    html_content = template.render(params.template_data)

    with open(
        settings.sendgrid.logo_url,
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
