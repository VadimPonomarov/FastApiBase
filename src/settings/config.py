import os

from celery import Celery
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Явно указываем путь к файлу .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)
print(f"Загружен .env файл по пути: {dotenv_path}")


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


class SendgridConfig(BaseSettingsBase):
    api_key: str | None = None


class Settings(BaseSettingsBase):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    celery_app: CeleryConfig = CeleryConfig()
    sendgrid: SendgridConfig = SendgridConfig()


settings = Settings()
