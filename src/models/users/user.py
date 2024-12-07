from models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from models.mixins.id_int import IdIntMixin


class UserModel(IdIntMixin, BaseModel):
    username: Mapped[str] = mapped_column(unique=True)
