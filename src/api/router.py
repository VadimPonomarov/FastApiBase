from fastapi import APIRouter

from core.settings.config import settings
from .hello_world import router as users_router

router = APIRouter(prefix=settings.api.prefix)
router.include_router(users_router)
