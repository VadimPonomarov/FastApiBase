import os

from loguru import logger

from settings.config import settings

os.makedirs(settings.log_directory, exist_ok=True)

ENABLE_LOGGING = settings.enable_logging

if ENABLE_LOGGING:
    logger.add(
        os.path.join(settings.log_directory, "app.log"),
        level=settings.log_level or "DEBUG",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="10 MB",
        compression="zip",
    )
else:
    logger.disable("loguru")  # Отключаем логирование

__all__ = ["logger"]
