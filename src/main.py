import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from api.endpoints import Router
from core.config import settings
from core.db_helper import db_helper
from core.enums.loguru_enums import LoguruFormatEnum

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
main_app.include_router(Router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
