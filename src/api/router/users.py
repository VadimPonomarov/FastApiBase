from fastapi import APIRouter

from api.dependencies.users_routes import fastapi_users
from core.schemas.user_manager import UserRead, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
router.include_router(
    fastapi_users.get_reset_password_router(),
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)