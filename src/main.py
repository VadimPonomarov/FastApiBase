import os
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from api.router import router
from core.enums import LoguruFormatEnum
from core.settings.config import settings
from core.utils.converters import str_to_bool

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if str_to_bool(os.getenv("APP_CONFIG__LOGURU", False)):
        logger.remove()
        logger.add(sink=sys.stdout, format=LoguruFormatEnum.BASE.value)
        logger.info("That's it, beautiful and simple logging!")
    yield
    logger.remove()


main_app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
main_app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
