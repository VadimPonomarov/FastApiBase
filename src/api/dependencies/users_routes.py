from fastapi import APIRouter
from fastapi_users import FastAPIUsers, schemas, models
from fastapi_users.authentication import AuthenticationBackend

from api.dependencies.authentication.auth_router import get_my_auth_router
from api.dependencies.authentication.backend import authentication_backend
from api.dependencies.authentication.user_manager import get_user_manager
from api.dependencies.authentication.verify_router import get_my_verify_router
from core.models.user.user_model import User
from core.types.user_types import UserIdType


class MyFastAPIUsers(FastAPIUsers[User, UserIdType]):

    def get_verify_router(self, user_schema: type[schemas.U]) -> APIRouter:
        return get_my_verify_router(self.get_user_manager, user_schema)

    def get_auth_router(
        self,
        backend: AuthenticationBackend[models.UP, models.ID],
        requires_verification: bool = False,
    ) -> APIRouter:
        """
        Return an auth router for a given authentication backend.

        :param backend: The authentication backend instance.
        :param requires_verification: Whether the authentication
        require the user to be verified or not. Defaults to False.
        """
        return get_my_auth_router(
            backend,
            self.get_user_manager,
            self.authenticator,
            requires_verification,
        )


fastapi_users = MyFastAPIUsers(
    get_user_manager,
    [authentication_backend],
)
