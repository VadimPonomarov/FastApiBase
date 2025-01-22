from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy

from api.dependencies.authentication.token_db import get_access_token_db
from core.config import settings

if TYPE_CHECKING:
    from core.models.token.access_token_model import AccessToken


def get_database_strategy(
    access_token_db: Annotated[
        AccessTokenDatabase["AccessToken"], Depends(get_access_token_db)
    ],
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db, lifetime_seconds=settings.auth.access_token_lifetime
    )
