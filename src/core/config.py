from typing import Annotated, Dict

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettingsBase(BaseSettings):
    __abstract__ = True
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env.example", ".env"),
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


class AuthConfig(BaseSettingsBase):
    login_url: str
    secret: str
    token_life: str


class DatabaseConfig(BaseSettingsBase):
    url: str
    echo: bool
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    naming_conventions: Annotated[
        Dict[str, str],
        Field(
            default_factory=lambda: {
                "ix": "ix_%(column_0_label)s",
                "uq": "uq_%(table_name)s_%(column_0_N_name)s",
                "ck": "ck_%(table_name)s_%(constraint_name)s",
                "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                "pk": "pk_%(table_name)s",
            }
        ),
    ]


class Settings(BaseSettingsBase):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    loguru: LoguruConfig = LoguruConfig()
    auth: AuthConfig = AuthConfig()
    db: DatabaseConfig


settings = Settings()  # type: ignore
