from fastapi import APIRouter

from api.dependencies.users_routes import fastapi_users
from core.schemas.user_manager import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)