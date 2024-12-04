from fastapi import APIRouter

router = APIRouter(
    prefix="/example",
    tags=["example"],
)


@router.get("/example")
async def example_route():
    return {"message": "This is an example route"}


__all__ = ["router"]
