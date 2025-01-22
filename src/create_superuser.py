import asyncio
import contextlib

from fastapi_users.exceptions import UserNotExists
from pydantic import BaseModel, EmailStr, ValidationError

from api.dependencies.authentication.user_db import get_user_db
from api.dependencies.authentication.user_manager import get_user_manager
from core.auth.user_manager import UserManager
from core.models import User
from core.schemas.user_manager import UserCreate
from core.utils.db_helper import db_helper

get_users_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user

async def check_email_exists(email: EmailStr) -> bool:
    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                try:
                    existing_user = await user_manager.get_by_email(email)
                    if existing_user:
                        print("A superuser with this email already exists. Please enter a different email.")
                        return True
                except UserNotExists:
                    return False

async def create_superuser(
    email: EmailStr,
    password: str,
):
    user_create = UserCreate(
        email=email,
        password=password,
        is_active=True,
        is_superuser=True,
        is_verified=True,
    )
    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )
                return True

class EmailModel(BaseModel):
    email: EmailStr

def get_valid_email():
    while True:
        email_input = input("Enter email: ")
        try:
            email = EmailModel(email=email_input).email
            return email
        except ValidationError as e:
            print(f"Invalid email: {e}")

async def main():
    while True:
        email = get_valid_email()
        if await check_email_exists(email):
            continue

        password = input("Enter password: ")

        if await create_superuser(
            email=email,
            password=password,
        ):
            print("Superuser created successfully.")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
    except EOFError:
        print("\nInput was interrupted. Exiting...")
















