from pydantic import BaseModel

from settings.config import settings


class MyTemplateData(BaseModel):
    title: str
    message: str
    logo_url: str


class SendEmailParams(BaseModel):
    from_email: str = settings.sendgrid.my_email
    to_email: str = settings.sendgrid.my_email
    subject: str = "Subject"
    template_data: dict[str, str]
