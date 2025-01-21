import os
from typing import Annotated, Dict

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


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


class ApiPrefix(BaseSettingsBase):
    prefix: str = Field(default="/api")


class AuthConfig(BaseSettingsBase):
    prefix: str = Field(default="/auth")
    login_url: str = Field(
        default_factory=lambda: os.getenv("APP_CONFIG__AUTH__LOGIN_URL")
    )
    secret: str = Field(default_factory=lambda: os.getenv("APP_CONFIG__AUTH__SECRET"))
    access_token_lifetime: int = Field(
        default_factory=lambda: int(os.getenv("APP_CONFIG__AUTH__TOKEN_LIFETIME", 3600))
    )


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
    auth: AuthConfig = AuthConfig()
    db: DatabaseConfig
    loguru: bool = Field(default_factory=lambda: os.getenv("APP_CONFIG__LOGURU", False))


settings = Settings()  # type: ignore
