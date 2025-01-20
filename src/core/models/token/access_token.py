from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.mixins.model_mixins.id_int_mixin import IdIntMixin
from core.mixins.model_mixins.model_relation_mixin import ModelRelationMixin
from core.models import BaseModel
from core.models.user.user_model import User
from core.types.user_types import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class AccessToken(
    IdIntMixin,
    BaseModel,
    ModelRelationMixin,
    SQLAlchemyBaseAccessTokenTable[UserIdType],
):
    _related_models = User

    @classmethod
    async def get_access_token_db(
        cls,
        session: "AsyncSession",
    ):
        yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
