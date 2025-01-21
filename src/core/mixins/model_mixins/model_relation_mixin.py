from typing import Type

from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.utils.converters import camel_case_to_snake_case

Base = declarative_base()


class ModelRelationMixin:
    _related_model: Type[Base]
    _related_model_id: str = "id"  # Значение по умолчанию
    _related_model_back_populates: str | None = None
    _related_model_id_nullable: bool = False
    _related_model_id_unique: bool = False

    @declared_attr
    @classmethod
    def related_model_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(f"{cls._related_model.__tablename__}.{cls._related_model_id}"),
            unique=cls._related_model_id_unique,
            nullable=cls._related_model_id_nullable,
        )

    @declared_attr
    @classmethod
    def related_model(cls) -> Mapped[str]:
        back_populates = (
            cls._related_model_back_populates
            or f"{camel_case_to_snake_case(cls.__name__)}s"
        )
        return relationship(
            cls._related_model,
            back_populates=back_populates,
        )

    @declared_attr
    @classmethod
    def related_models(cls) -> Mapped[list[str]]:
        back_populates = (
            cls._related_model_back_populates
            or f"{camel_case_to_snake_case(cls.__name__)}s"
        )
        return relationship(
            cls._related_model,
            back_populates=back_populates,
        )
