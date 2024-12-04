# Third Party Libraries
from fastapi import APIRouter

# Project Dependencies
from core.config import settings

router = APIRouter(
    prefix=settings.api.prefix,
    tags=["example"],
)


@router.get("/example")
async def example_route():
    return {"message": "This is an example route"}


__all__ = ["router"]
