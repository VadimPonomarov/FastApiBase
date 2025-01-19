from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from core.settings.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False, autocommit=False
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_get(self):
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
)
