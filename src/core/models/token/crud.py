from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models import AccessToken
from core.models.token.refresh_token_model import RefreshToken
from core.types.user_types import UserIdType


class TokenRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_access_token(self, token: str, user_id: UserIdType):
        db_token = AccessToken(token=token, user_id=user_id)
        self.db.add(db_token)
        await self.db.commit()
        await self.db.refresh(db_token)
        return db_token

    async def create_refresh_token(self, token: str, user_id: UserIdType):
        db_token = RefreshToken(token=token, user_id=user_id)
        self.db.add(db_token)
        await self.db.commit()
        await self.db.refresh(db_token)
        return db_token

    async def get_access_token(self, token: str):
        result = await self.db.execute(
            select(AccessToken).filter(AccessToken.token == token)
        )
        return result.scalars().first()

    async def get_refresh_token(self, token: str):
        result = await self.db.execute(
            select(RefreshToken).filter(RefreshToken.token == token)
        )
        return result.scalars().first()

    async def delete_access_token(self, token: str):
        db_token = await self.get_access_token(token)
        if db_token:
            await self.db.delete(db_token)
            await self.db.commit()

    async def delete_refresh_token(self, token: str):
        db_token = await self.get_refresh_token(token)
        if db_token:
            await self.db.delete(db_token)
            await self.db.commit()

    async def delete_all_access_tokens(self, user_id: UserIdType):
        await self.db.execute(delete(AccessToken).where(AccessToken.user_id == user_id))
        await self.db.commit()

    async def delete_all_refresh_tokens(self, user_id: UserIdType):
        await self.db.execute(
            delete(RefreshToken).where(RefreshToken.user_id == user_id)
        )
        await self.db.commit()
