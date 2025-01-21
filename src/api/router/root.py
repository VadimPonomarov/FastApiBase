from fastapi import APIRouter

from core.config import settings
from .auth import router as auth_router

root_router = APIRouter(
    prefix=settings.api.prefix,
)
root_router.include_router(auth_router)
