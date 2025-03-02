from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.mail_services import send_email

router = APIRouter()


class EmailSchema(BaseModel):
    to_email: str
    subject: str
    message: str


@router.post("/send-email/")
async def send_email_endpoint(email: EmailSchema):
    try:
        template_data = {
            "title": email.subject,
            "message": email.message,
            "logo_url": "cid:logo",
        }
        send_email.delay(email.to_email, email.subject, template_data)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
