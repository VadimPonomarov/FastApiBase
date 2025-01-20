from sqlalchemy.orm import Mapped, mapped_column

from core.mixins.model_mixins.datetime_mixin import CrtUpdDatetimeMixin
from core.mixins.model_mixins.id_int_mixin import IdIntMixin
from core.mixins.model_mixins.model_relation_mixin import ModelRelationMixin
from core.models import BaseModel
from core.models.user.user_model import User


class Profile(IdIntMixin, CrtUpdDatetimeMixin, ModelRelationMixin, BaseModel):
    _related_model = User
    name: Mapped[str] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
