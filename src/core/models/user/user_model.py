from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from core.mixins.model_mixins.datetime_mixin import CrtUpdDatetimeMixin
from core.mixins.model_mixins.id_int_mixin import IdIntMixin
from core.models import BaseModel
from core.types.user_types import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(
    IdIntMixin, CrtUpdDatetimeMixin, BaseModel, SQLAlchemyBaseUserTable[UserIdType]
):
    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
