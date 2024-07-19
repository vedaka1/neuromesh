import logging
import os
from functools import lru_cache
from typing import Generator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from application.common.tg_client import AsyncTGClient
from src.infrastructure.config import settings
from src.infrastructure.di.container import (
    DatabaseAdaptersProvider,
    DatabaseConfigurationProvider,
    ImagesProvider,
    UseCasesProvider,
)
from src.infrastructure.persistence.main import create_engine, create_session_factory
from src.infrastructure.persistence.models import *
from src.infrastructure.persistence.repositories import *

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer(
        image="postgres:15-alpine",
        username="username",
        password="password",
        dbname="terra",
    )
    if os.name == "nt":
        postgres.get_container_host_ip = lambda: "localhost"
    try:
        postgres.start()
        postgres_url_ = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        logger.info("postgres url %s", postgres_url_)
        yield postgres_url_
    finally:
        postgres.stop()


@pytest.fixture(scope="session", autouse=True)
async def setup_db(postgres_url: str):
    engine = create_engine(postgres_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture
def container(postgres_url: str):
    from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

    class SettingsProvider(Provider):
        @provide(scope=Scope.APP)
        def engine(self) -> AsyncEngine:
            return create_engine(db_url=postgres_url)

        @provide(scope=Scope.APP)
        def session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
            return create_session_factory(engine)

        @provide(scope=Scope.APP)
        def tg_client(self) -> AsyncTGClient:
            return AsyncClient(base_url=settings.TG_API)

    @lru_cache(1)
    def get_container() -> AsyncContainer:
        return make_async_container(
            SettingsProvider(),
            DatabaseConfigurationProvider(),
            DatabaseAdaptersProvider(),
            UseCasesProvider(),
            ImagesProvider(),
        )

    container = get_container()
    yield container


@pytest.fixture
def client():
    client = AsyncClient()
    yield client
