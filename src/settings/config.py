from typing import Literal

from celery import Celery
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettingsBase(BaseSettings):
    __abstract__ = True
    model_config = SettingsConfigDict(
        env_file=[".env.template", ".env.example", ".env"],
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="allow",
        arbitrary_types_allowed=True,
    )


class RunConfig(BaseSettingsBase):
    host: str = Field(default="localhost")
    port: int = Field(default=8000)
    docker: bool | None = None


class ApiPrefix(BaseSettingsBase):
    prefix: str = Field(default="/api")


class CeleryConfig(BaseSettingsBase):
    celery_broker: str | None = None
    celery_backend: str | None = None
    celery_include: str | None = None

    @property
    def get_celery_app(self) -> Celery:
        celery_app = Celery(
            "config",
            broker=self.celery_broker,
            backend=self.celery_backend,
            broker_connection_retry_on_startup=True,
            include=self.celery_include.split(",") if self.celery_include else [],
        )

        celery_app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="Europe/Kiev",
            enable_utc=True,
        )

        return celery_app


class PikaConfig(BaseSettingsBase):
    connection_param: str | None = None


class SendgridConfig(BaseSettingsBase):
    api_key: str | None = None
    my_email: str | None = None


class Settings(BaseSettingsBase):
    environment: Literal["dev", "prod"] = "dev"
    enable_logging: bool = True
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_directory: str = "./logs"
    media_path: str | None = "./media"
    templates_path: str | None = "./templates"
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    celery_app: CeleryConfig = CeleryConfig()
    sendgrid: SendgridConfig = SendgridConfig()
    pika: PikaConfig = PikaConfig()


settings = Settings()
