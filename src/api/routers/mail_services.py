import os
from base64 import b64encode

import sendgrid
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from sendgrid.helpers.mail import Attachment, Mail

load_dotenv()

# Настройка Jinja2 для загрузки шаблонов из папки 'templates'
template_loader = FileSystemLoader(searchpath="./templates")
env = Environment(loader=template_loader, autoescape=True)


def send_email(to_email: str, subject: str, template_data: dict):
    # Загрузка и рендеринг HTML-шаблона
    template = env.get_template("email_template.html")
    html_content = template.render(template_data)

    # Чтение логотипа и кодирование в base64
    with open("../public/indonesian_halal_logo_2022.jpg", "rb") as logo_file:
        logo_data = logo_file.read()
        encoded_logo = b64encode(logo_data).decode()

    # Создание вложения для логотипа
    attachment = Attachment()
    attachment.file_content = encoded_logo
    attachment.file_type = "image/png"
    attachment.file_name = "logo.png"
    attachment.disposition = "inline"
    attachment.content_id = "logo"

    # Создание сообщения
    message = Mail(
        from_email="pvs.versia@gmail.com",
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )
    message.add_attachment(attachment)

    # Отправка сообщения через SendGrid API
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
