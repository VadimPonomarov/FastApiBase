from celery import Celery

celery_app = Celery(
    "celery_config",
    broker="pyamqp://guest:guest@localhost:5672//",
    backend="rpc://",
    include=["api.routers.mail_services"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Kiev",
    enable_utc=True,
)
