from pydantic import Field, PostgresDsn, field_validator
from typing import Annotated
from loguru import logger
from pydantic_settings import SettingsConfigDict, BaseSettings

logger.name = "my_loguru_logger"


class BaseSettingsBase(BaseSettings):
    __abstract__ = True
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="allow",
    )


class RunConfig(BaseSettingsBase):
    host: str = Field(default="localhost")
    port: int = Field(default=8000)


class LoguruConfig(BaseSettingsBase):
    is_logging: bool = True

    @field_validator("is_logging", mode="before")
    def convert_to_bool(cls, value):
        if isinstance(value, str):
            if value.lower() in ["true", "1"]:
                return bool(True)
            elif value.lower() in ["false", "0"]:
                return bool(False)
        return value


class ApiPrefix(BaseSettingsBase):
    prefix: str = Field(default="/api")


class DatabaseConfig(BaseSettingsBase):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: Annotated[dict[str, str], Field(default={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })]


class Settings(BaseSettingsBase):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    loguru: LoguruConfig = LoguruConfig()
    db: DatabaseConfig


settings = Settings()
