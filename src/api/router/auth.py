from fastapi.routing import APIRouter

from api.dependencies.authentication.backend import authentication_backend
from api.dependencies.users_routes import fastapi_users
from core.config import settings

router = APIRouter(prefix=settings.auth.prefix, tags=["Auth"])

router.include_router(router=fastapi_users.get_auth_router(authentication_backend))
