from fastapi import APIRouter

from api.users.views import say_hello

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def hello():
    return await say_hello()
