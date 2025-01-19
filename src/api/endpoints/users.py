from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/items/{hello}")
async def read_item(hello: Annotated[str, Path(default_factory=lambda: "hello")]):
    return {"hello": hello}
