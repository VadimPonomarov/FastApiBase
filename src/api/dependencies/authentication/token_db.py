from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from core.models.token.access_token_model import AccessToken
from core.utils.db_helper import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: Annotated["AsyncSession",Depends(db_helper.session_get)],
):
    yield AccessToken.get_db(session=session)
