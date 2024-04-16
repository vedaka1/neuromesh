import asyncio

import asyncpg
import pytest
from httpx import AsyncClient
from punq import Container, Scope

from src.domain.users.repository import BaseUserRepository
from src.infrastructure.config import settings
from src.infrastructure.persistence.database import DatabaseResource
from src.infrastructure.persistence.repositories.user import UserRepository

# @pytest.fixture(scope="session")
# async def create_connection() -> AsyncGenerator[Any, asyncpg.Connection]:
#     connection: asyncpg.Connection = await asyncpg.connect(settings.DB_URL)
#     yield connection
#     await connection.close()


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture(scope="session", autouse=True)
# async def init_connection_pool():
#     pool: asyncpg.Pool = await asyncpg.create_pool(settings.DB_URL)
#     yield pool


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    connection: asyncpg.Connection = await asyncpg.connect(settings.DB_URL)
    await connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            is_premium BOOLEAN DEFAULT FALSE
        );
        """
    )
    yield
    await connection.execute("DROP TABLE users;")


@pytest.fixture(scope="session")
def client():
    client = AsyncClient()
    yield client


@pytest.fixture(scope="session")
async def container() -> Container:
    container = Container()
    container.register(
        DatabaseResource,
        instance=DatabaseResource(settings.DB_URL),
        scope=Scope.singleton,
    )

    async def init_user_repository() -> UserRepository:
        db: DatabaseResource = container.resolve(DatabaseResource)
        user_repository = UserRepository(connection=await db.get_connection())
        return user_repository

    container.register(
        BaseUserRepository, factory=init_user_repository, scope=Scope.transient
    )
    return container
