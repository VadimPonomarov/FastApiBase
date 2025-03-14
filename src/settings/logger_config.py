from loguru import logger

from settings.config import settings

ENABLE_LOGGING = settings.enable_logging

if ENABLE_LOGGING:
    logger.add(sink="stdout", level=settings.log_level or "DEBUG")
else:
    logger.remove()

__all__ = ["logger"]
