from typing import Annotated, Dict

from pydantic import Field, PostgresDsn, computed_field
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


class ApiPrefix(BaseSettingsBase):
    prefix: str = Field(default="/api")


class DatabaseConfig(BaseSettingsBase):
    scheme: str = "postgresql+asyncpg"
    db: str = "postgres"
    user: str = "postgres"
    password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432
    echo: bool = True
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

    @computed_field
    def url(self) -> PostgresDsn:
        return PostgresDsn(
            url=f"{self.scheme}://{self.user}:{self.password}@{self.db_host}:{self.db_port}/{self.db}"
        )


class Settings(BaseSettingsBase):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()  # type: ignore
