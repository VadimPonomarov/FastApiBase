# Third Party Libraries
import uvicorn
from fastapi import FastAPI

# Project Dependencies
from api import router
from core.config import settings

app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
