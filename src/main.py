import asyncio
from contextlib import asynccontextmanager

import pika
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from services.mail_services import send_email
from services.pika_helper import ConnectionFactory
from settings.config import settings
from settings.logger_config import logger  # noqa.

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = asyncio.create_task(start_consumer())
    logger.info("Starting rabbitmq consumer  ...")
    yield

    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
    logger.info("Application shutdown completed.")


async def start_consumer():
    def consume():
        connection = ConnectionFactory(
            pika.ConnectionParameters("rabbitmq"),
            "email_queue",
            callback=lambda *args, **kwargs: send_email.delay(*args, **kwargs),
        )
        connection.consume()

    await asyncio.to_thread(consume)


main_app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
