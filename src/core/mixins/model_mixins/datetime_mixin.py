from sqlalchemy import DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column


class CrtUpdDatetimeMixin:
    @declared_attr
    @classmethod
    def created_at(cls) -> Mapped[DateTime]:
        return mapped_column(DateTime, server_default=func.now(), nullable=False)

    @declared_attr
    @classmethod
    def updated_at(cls) -> Mapped[DateTime]:
        return mapped_column(
            DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
        )
