from fastapi import APIRouter

from settings.config import settings
from .routers.mail_router import router as mail_router

router = APIRouter(prefix=settings.api.prefix)
router.include_router(mail_router)
