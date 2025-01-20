from typing import Annotated, Generator, Type, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.db_helper import db_helper

T = TypeVar("T")


async def get_db(
    model: Type[T], session: Annotated[AsyncSession, Depends(db_helper.session_get)]
) -> Generator[T, None, None]:
    yield model.get_db(session=session)
