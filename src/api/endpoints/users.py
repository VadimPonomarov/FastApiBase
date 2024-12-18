# Third Party Libraries
from fastapi import APIRouter

from crud.users import say_hello

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def hello():
    return await say_hello()
