from base64 import b64encode

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment, Mail

from celery_config import celery_app
from core.enums.templates import TemplatesEnum, TemplatesLogosEnum
from settings.config import settings

load_dotenv()

template_loader = FileSystemLoader(searchpath="./templates")
env = Environment(loader=template_loader, autoescape=True)


@celery_app.task(name="send_email_task")
def send_email(to_email: str, subject: str, template_data: dict):
    template = env.get_template(TemplatesEnum.EMAIL_TEMPLATE_BASE.value)
    html_content = template.render(template_data)

    with open(
        f"./media/{TemplatesLogosEnum.INDONESIAN_HALAL_LOGO.value}",
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
        from_email=settings.sendgrid.my_email,
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
