from fastapi.routing import APIRouter

from api.dependencies.authentication.backend import authentication_backend
from api.dependencies.users_routes import fastapi_users
from core.config import settings
from core.schemas.user_manager import UserCreate, UserRead

router = APIRouter(prefix=settings.auth.prefix, tags=["Auth"])
router.include_router(router=fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(router=fastapi_users.get_auth_router(authentication_backend))
router.include_router(router=fastapi_users.get_verify_router(UserRead))
router.include_router(router=fastapi_users.get_reset_password_router())

