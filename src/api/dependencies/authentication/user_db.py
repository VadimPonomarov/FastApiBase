from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from core.models.user.user_model import User
from core.utils.db_helper import db_helper

if TYPE_CHECKING:
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(
    session: Annotated["AsyncSession", Depends(db_helper.session_get)]
)-> "SQLAlchemyUserDatabase":
    yield User.get_db(session=session)
