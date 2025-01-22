from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from api.dependencies.authentication.user_db import get_user_db
from core.auth.user_manager import UserManager

if TYPE_CHECKING:
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_manager(
    users_db: Annotated[
        "SQLAlchemyUserDatabase",
        Depends(get_user_db),
    ]
)-> UserManager:
    yield UserManager(users_db)
