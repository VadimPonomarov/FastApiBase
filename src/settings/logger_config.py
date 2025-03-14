import os

from loguru import logger

from settings.config import settings

log_directory = settings.log_directory
os.makedirs(log_directory, exist_ok=True)

if settings.enable_logging:
    logger.add(
        os.path.join(log_directory, "app.log"),
        level=settings.log_level or "DEBUG",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="10 MB",
        compression="zip",
    )
else:
    logger.disable("loguru")

__all__ = ["logger"]
