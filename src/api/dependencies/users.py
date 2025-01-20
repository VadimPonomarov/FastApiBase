from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from core.models.user.user_model import User
from core.utils.db_helper import db_helper

from ...core.utils.database import get_db

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(
    session: Annotated["AsyncSession", Depends(db_helper.session_get)]
):
    async for item in get_db(User, session):
        yield item
