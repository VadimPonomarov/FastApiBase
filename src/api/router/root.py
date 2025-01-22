from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .auth import router as auth_router
from .users import router as users_router

http_bearer = HTTPBearer(auto_error=False)
root_router = APIRouter(
    prefix=settings.api.prefix,
    dependencies=[Depends(http_bearer)],
)
root_router.include_router(auth_router)
root_router.include_router(users_router)
