import asyncio
import logging
from functools import lru_cache

from application.common.transaction import ICommiter
from application.usecases.neural_networks import *
from application.usecases.subscriptions import *
from application.usecases.users import *
from domain.neural_networks.manager import BaseModelManager
from domain.neural_networks.repository import (
    BaseNeuralNetworkRepository,
    BaseNeuralNetworkSubscriptionRepository,
)
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import (
    BaseUserRepository,
    BaseUserRequestRepository,
    BaseUserSubscriptionRepository,
)
from punq import Container, Scope
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infrastructure.neural_networks.main import ModelManager
from infrastructure.persistence.main import create_engine, create_session_factory
from infrastructure.persistence.repositories import (
    NeuralNetworkRepository,
    NeuralNetworkSubscriptionRepository,
    SubscriptionRepository,
    UserRepository,
    UserRequestRepository,
    UserSubscriptionRepository,
)
from infrastructure.persistence.transaction import Commiter


@lru_cache(1)
def get_container() -> Container:
    container = init_container()
    print('INITIALIZED')
    return container


@lru_cache(1)
def init_logger() -> None:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding='UTF-8',
        format='%(asctime)s %(levelname)s: %(message)s',
    )
    return None


def init_container() -> Container:
    container = Container()
    engine = create_engine()
    session_factory = create_session_factory(engine)

    container.register('lifespan_engine', instance=engine)

    async def session_generator():
        session = session_factory()
        yield session
        await session.close()

    session = session_generator()

    def get_session():
        loop = asyncio.get_running_loop()
        new_session = asyncio.gather(session.__anext__(), return_exceptions=False)
        return new_session

    container.register(async_sessionmaker, instance=session_factory, scope=Scope.singleton)

    container.register(AsyncSession, factory=get_session, scope=Scope.transient)
    container.register(ICommiter, Commiter, scope=Scope.transient)
    container.register(BaseModelManager, ModelManager, scope=Scope.singleton)
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
    container.register(
        BaseUserRequestRepository,
        UserRequestRepository,
        scope=Scope.transient,
    )
    container.register(
        BaseUserSubscriptionRepository,
        UserSubscriptionRepository,
        scope=Scope.transient,
    )
    container.register(
        BaseNeuralNetworkSubscriptionRepository,
        NeuralNetworkSubscriptionRepository,
        scope=Scope.transient,
    )
    # Users usecases
    container.register(GetAllUsers, scope=Scope.transient)
    container.register(UpdateUserSubscription, scope=Scope.transient)
    container.register(CreateUser, scope=Scope.transient)
    container.register(DeleteUser, scope=Scope.transient)
    container.register(GetAllUsers, scope=Scope.transient)
    container.register(GetUserByTelegramId, scope=Scope.transient)
    container.register(GetUserRequests, scope=Scope.transient)
    container.register(GetUserSubscriptions, scope=Scope.transient)
    container.register(UpdateUserRequests, scope=Scope.transient)

    # Subscriptions usecases
    container.register(CreateSubscription, scope=Scope.transient)
    container.register(AddModelToSubscription, scope=Scope.transient)
    container.register(GetAllSubscriptions, scope=Scope.transient)
    container.register(GetSubscriptionByName, scope=Scope.transient)

    # Neural networks usecases
    container.register(CreateNeuralNetwork, scope=Scope.transient)
    container.register(GenerateResponse, scope=Scope.transient)
    container.register(GetAllNeuralNetworks, scope=Scope.transient)
    container.register(GetNeuralNetworkByName, scope=Scope.transient)

    return container
