from fastapi import APIRouter
from fastapi_users import FastAPIUsers, schemas

from api.dependencies.authentication.backend import authentication_backend
from api.dependencies.authentication.user_manager import get_user_manager
from api.dependencies.authentication.verify_router import get_my_verify_router
from core.models.user.user_model import User
from core.types.user_types import UserIdType


class MyFastAPIUsers(FastAPIUsers[User, UserIdType]):

    def get_verify_router(self, user_schema: type[schemas.U]) -> APIRouter:
        return get_my_verify_router(self.get_user_manager, user_schema)


fastapi_users = MyFastAPIUsers(
    get_user_manager,
    [authentication_backend],
)
