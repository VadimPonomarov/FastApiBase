# Third Party Libraries
from contextlib import asynccontextmanager

import uvicorn

# Project Dependencies
from api import router
from core import db_helper, settings
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("Disposing")
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
