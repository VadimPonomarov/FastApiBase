from typing import TYPE_CHECKING, Annotated

from api.dependencies.authentication.user_db import get_user_db
from core.auth.user_manager import UserManager
from core.models.user.user_model import User
from core.utils.database import get_db
from core.utils.db_helper import db_helper

from fastapi import Depends

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_manager(
    user_db: Annotated["SQLAlchemyUserDatabase", Depends(get_user_db)]
):
    yield UserManager(user_db)
