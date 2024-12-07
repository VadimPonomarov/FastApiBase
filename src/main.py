import sys
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from core.enums.loguru_enums import LoguruFormatEnum
from models.base import BaseModel
from models.db_helper import db_helper
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.loguru.is_logging:
        logger.remove()
        logger.add(sink=sys.stdout, format=LoguruFormatEnum.BASE.value)
        logger.info("That's it, beautiful and simple logging!")
    yield
    logger.remove()
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
