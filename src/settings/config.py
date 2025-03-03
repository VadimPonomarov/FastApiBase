from celery import Celery
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettingsBase(BaseSettings):
    __abstract__ = True
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env.example", ".env"),
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


class CeleryConfig(BaseModel):
    broker: str = Field(default="pyamqp://guest:guest@localhost:5672//")
    backend: str = Field(default="rpc://")
    include: str = Field(default="services")

    def get_celery_app(self) -> Celery:
        celery_app = Celery(
            "config",
            broker=self.broker,
            backend=self.backend,
            include=self.include.split(","),
        )

        celery_app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="Europe/Kiev",
            enable_utc=True,
        )

        return celery_app


class Settings(BaseSettingsBase):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    celery_app: Celery = CeleryConfig().get_celery_app()


settings = Settings()
