from fastapi.routing import APIRouter
import fastapi_users.router

from api.dependencies.authentication.backend import authentication_backend
from core.config import settings

router = APIRouter(prefix=settings.auth.prefix, tags=["Auth"])

router.include_router(
    router=fastapi_users.router.get_oauth_router(authentication_backend)
)
