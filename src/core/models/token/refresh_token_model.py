from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from core.models import BaseModel
from core.types.user_types import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class RefreshToken(BaseModel, SQLAlchemyBaseAccessTokenTable[UserIdType]):
    token: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, primary_key=True
    )
    user_id: Mapped[UserIdType] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    @classmethod
    def get_db(
        cls,
        session: "AsyncSession",
    ):
        return SQLAlchemyAccessTokenDatabase(session, cls)
