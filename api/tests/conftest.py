import asyncio

import pytest
from httpx import AsyncClient
from punq import Container, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from src.domain.neural_networks.repository import BaseNeuralNetworkRepository
from src.domain.subscriptions.repository import BaseSubscriptionRepository
from src.domain.users.repository import BaseUserRepository
from src.infrastructure.persistence.main import create_engine, create_session_factory
from src.infrastructure.persistence.models import *
from src.infrastructure.persistence.repositories import *
from src.infrastructure.persistence.repositories.user import UserRepository


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    engine = create_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def container():
    container = Container()
    engine = create_engine()
    container.register(AsyncEngine, instance=engine)
    session_factory = create_session_factory(engine)
    container.register(async_sessionmaker, instance=session_factory)

    container.register(
        BaseUserRepository,
        UserRepository,
        scope=Scope.transient,
    )
    container.register(
        BaseSubscriptionRepository,
        SubscriptionRepository,
        scope=Scope.transient,
    )
    container.register(
        BaseNeuralNetworkRepository,
        NeuralNetworkRepository,
        scope=Scope.transient,
    )
    yield container


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client():
    client = AsyncClient()
    yield client
