import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from api.endpoints.router import router
from core.db import db_helper
from core.enums import LoguruFormatEnum
from core.settings.config import settings

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.loguru.is_logging:
        logger.remove()
        logger.add(sink=sys.stdout, format=LoguruFormatEnum.BASE.value)
        logger.info("That's it, beautiful and simple logging!")
    yield
    logger.remove()
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
main_app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
