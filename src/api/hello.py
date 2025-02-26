from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(prefix="", tags=["Hello"])


@router.get("/")
async def read_item(hello: Annotated[str, Path(default_factory=lambda: "hello")]):
    return "Hello, World"
