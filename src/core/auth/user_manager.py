from typing import TYPE_CHECKING, Optional

from fastapi_users import BaseUserManager

from core.config import settings
from core.mixins.model_mixins.id_int_mixin import IdIntMixin
from core.models.user.user_model import User
from core.types.user_types import UserIdType

if settings.loguru:
    from loguru import logger

    logger = logger.bind(name="auth")

if TYPE_CHECKING:
    from fastapi import Request


class UserManager(IdIntMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.auth.secret
    verification_token_secret = settings.auth.secret

    def parse_id(self, user_id: str) -> int: return int(user_id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional["Request"] = None
    ):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional["Request"] = None
    ):
        logger.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )
