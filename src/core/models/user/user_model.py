from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from core.mixins.model_mixins.datetime_mixin import CrtUpdDatetimeMixin
from core.mixins.model_mixins.id_int_mixin import IdIntMixin
from core.models import BaseModel


class User(BaseModel, IdIntMixin, CrtUpdDatetimeMixin, SQLAlchemyBaseUserTable[int]):
    pass
