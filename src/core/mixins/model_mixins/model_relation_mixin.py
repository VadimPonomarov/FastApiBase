from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.utils import camel_case_to_snake_case


class ModelRelationMixin:
    _related_model: str
    _related_model_id: str = "id"
    _related_model_back_populates: str | None = None
    _related_model_id_nullable: bool = False
    _related_model_id_unique: bool = False

    @declared_attr
    def related_model_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(f"{cls._related_model}.{cls._related_model_id}"),
            unique=cls._related_model_id_unique,
            nullable=cls._related_model_id_nullable,
        )

    @declared_attr
    def related_model(cls) -> Mapped:
        back_populates = (
            cls._related_model_back_populates
            or f"{camel_case_to_snake_case(cls.__name__)}s"
        )
        return relationship(
            cls._related_model,
            back_populates=back_populates,
        )

    @declared_attr
    def related_models(cls) -> Mapped:
        back_populates = (
            cls._related_model_back_populates
            or f"{camel_case_to_snake_case(cls.__name__)}s"
        )
        return relationship(
            cls._related_model,
            back_populates=back_populates,
        )
