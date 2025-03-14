import asyncio
from contextlib import asynccontextmanager

import pika
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from services.mail_services import send_email
from services.pika_helper import ConnectionFactory
from settings.config import settings

load_dotenv()

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = asyncio.create_task(start_consumer())
    yield
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass
    logger.info("Application shutdown completed.")


async def start_consumer():
    def consume():
        connection = ConnectionFactory(
            pika.ConnectionParameters("localhost"),
            "email_queue",
            callback=lambda *args, **kwargs: send_email.delay(*args, **kwargs),
        )
        connection.consume()

    await asyncio.to_thread(consume)


main_app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)

if __name__ == "__main__":
    if settings.environment == "dev":
        uvicorn.run(
            app="main:main_app",
            host=settings.run.host,
            port=settings.run.port,
            reload=True,
        )
    elif settings.environment == "prod":
        uvicorn.run(
            app="main:main_app",
            host=settings.run.host,
            port=settings.run.port,
            reload=False,
        )
    else:
        raise ValueError(f"Unknown environment: {settings.environment}")
