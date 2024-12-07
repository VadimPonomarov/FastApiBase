# Third Party Libraries
from fastapi import APIRouter

router = APIRouter(tags=["Users"])


@router.get("/")
async def get_users():
    return {"message": "Hello World"}
