import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from loguru import logger

from api.router import root_router
from core.config import settings
from core.enums import LoguruFormatEnum
from core.utils.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.loguru:
        logger.remove()
        logger.add(sink=sys.stdout, format=LoguruFormatEnum.BASE.value)
        logger.info("That's it, beautiful and simple logging!")
    yield
    logger.remove()
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
main_app.add_middleware(
CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
main_app.include_router(root_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        # log_level="error",
    )

    # uvicorn.run(app="main:main_app", host="0.0.0.0", port=8000, reload=True)
