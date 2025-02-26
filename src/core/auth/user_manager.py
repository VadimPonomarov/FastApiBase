from typing import TYPE_CHECKING, Optional

from fastapi import Request, Response
from fastapi_users import BaseUserManager, exceptions, jwt, models
from fastapi_users.jwt import JWT_ALGORITHM, generate_jwt
import jwt
from loguru import logger

from core.config import settings
from core.mixins import IdIntMixin
from core.models import User
from core.models.token.crud import TokenRepository
from core.types.user_types import UserIdType
from core.utils.db_helper import db_helper

if TYPE_CHECKING:
    from api.dependencies.authentication.auth_router import (
        HTTPBasicCredentialsWithEmail,
    )


class UserManager(IdIntMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.auth.secret
    verification_token_secret = settings.auth.secret
    access_token_lifetime_seconds = 3600
    refresh_token_lifetime_seconds = 86400

    def parse_id(self, user_id: str) -> int:
        return int(user_id)

    async def authenticate(
        self, credentials: "HTTPBasicCredentialsWithEmail"
    ) -> Optional[models.UP]:
        """
        Authenticate and return a user following an email and a password.

        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """
        try:
            user = await self.get_by_email(credentials.email)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        async for session in db_helper.session_get():
            token_repo = TokenRepository(session)

            # Удаление всех предыдущих токенов
            await token_repo.delete_all_access_tokens(user.id)
            await token_repo.delete_all_refresh_tokens(user.id)

            access_token_data = {"user_id": str(user.id)}
            access_token = generate_jwt(
                access_token_data,
                self.verification_token_secret,
                self.access_token_lifetime_seconds,
            )

            refresh_token_data = {"user_id": str(user.id)}
            refresh_token = generate_jwt(
                refresh_token_data,
                self.verification_token_secret,
                self.refresh_token_lifetime_seconds,
            )

            await token_repo.create_access_token(access_token, user.id)
            await token_repo.create_refresh_token(refresh_token, user.id)

            logger.info(
                f"User {user.id} logged in. Access token: {access_token}, Refresh token: {refresh_token}"
            )

            if response:
                response.set_cookie(
                    key="access_token", value=access_token, httponly=True
                )
                response.set_cookie(
                    key="refresh_token", value=refresh_token, httponly=True
                )

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }

    async def refresh_auth_tokens(self, refresh_token: str) -> Optional[User]:
        async for session in db_helper.session_get():
            token_repo = TokenRepository(session)
            token = await token_repo.get_refresh_token(refresh_token)
            if token is None:
                return None
            try:
                data = jwt.decode(
                    refresh_token,
                    self.verification_token_secret,
                    algorithms=JWT_ALGORITHM,
                )
                user_id = data.get("user_id")
                if user_id is None:
                    return None

                # Преобразование user_id в integer
                user_id = int(user_id)

                return await self.get(user_id)
            except Exception as e:
                logger.error(f"Error decoding refresh token: {e}")
                return None
