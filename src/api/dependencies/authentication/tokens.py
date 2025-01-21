from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.database import get_db
from core.utils.db_helper import db_helper

if TYPE_CHECKING:
    from core.models.token.access_token import AccessToken


async def get_access_token_db(
    session: Annotated["AsyncSession", Depends(db_helper.session_get)],
):
    async for item in get_db(AccessToken, session):
        yield item
