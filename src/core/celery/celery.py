from celery import Celery

app = Celery(
    "celery",
    broker="amqp://",
    backend="rpc://",
    include=["api.routers.mail_services"],
)
