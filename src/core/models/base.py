from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.utils import camel_case_to_snake_case


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    @classmethod
    def __tablename__(cls):
        return f"{camel_case_to_snake_case(cls.__name__)}s"
