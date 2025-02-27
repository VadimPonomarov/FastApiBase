
from pydantic import Field
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



class Settings(BaseSettingsBase):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()  # type: ignore
