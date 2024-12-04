# Third Party Libraries
from fastapi import APIRouter

# Project Dependencies
from api.users import router_users
from core.config import settings

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(router_users, tags=["Users"])


__all__ = ["router"]
