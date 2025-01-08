from typing import AsyncIterable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from infrastructure.config import config


def create_engine(db_url: str = config.db.DB_URL) -> AsyncEngine:
    return create_async_engine(db_url, echo=False)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterable[AsyncSession]:
    async with session_factory() as session:
        yield session
