import sys
from contextlib import asynccontextmanager

import uvicorn
from api import router
from core import db_helper, settings
from core.enums.loguru_enums import LoguruFormat
from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.loguru.is_logging:
        logger.remove()
        logger.add(sink=sys.stdout, format=LoguruFormat.BASE.value)
        logger.add(sink="test.log", format=LoguruFormat.BASE.value)
        logger.info("That's it, beautiful and simple logging!")
    yield
    logger.remove()
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
