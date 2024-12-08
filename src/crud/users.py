from pydantic import json


async def say_hello() -> json:
    return {"message": "Hello World!!!"}
