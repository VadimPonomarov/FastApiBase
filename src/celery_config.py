import os

from celery import Celery

# Загрузка переменных окружения из файла .env
from dotenv import load_dotenv

load_dotenv()

# Создание экземпляра Celery
celery_app = Celery(
    "email_tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

celery_app.conf.update(
    {
        "broker_url": os.getenv("CELERY_BROKER_URL"),
        "result_backend": os.getenv("CELERY_RESULT_BACKEND"),
    }
)


# Функция для отправки писем
@celery_app.task
def send_email_task(to_email, subject, template_data):
    from email_service import send_email

    send_email(to_email, subject, template_data)
