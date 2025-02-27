import os
from base64 import b64encode

import sendgrid
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from sendgrid.helpers.mail import Attachment, Mail

load_dotenv()

template_loader = FileSystemLoader(searchpath="./templates")
env = Environment(loader=template_loader, autoescape=True)

template = env.get_template("email_template.html")
data = {
    "title": "Welcome to Our Service",
    "message": "We are excited to have you on board. Enjoy our awesome service!",
}
html_content = template.render(data)

with open(
    r"..\public\indonesian_halal_logo_2022.jpg",
    "rb",
) as logo_file:
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
    to_emails="pvs.versia@gmail.com",
    subject=data["title"],
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
