import logging
from functools import lru_cache

from punq import Container, Scope
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.common.transaction import BaseTransactionManager
from application.usecases.neural_network import NeuralNetworkService
from application.usecases.subscription import SubscriptionService
from application.usecases.user import UserService
from application.usecases.users import *
from application.usecases.users.get_all_users import GetAllUsers
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
from infrastructure.persistence.transaction import TransactionManager


@lru_cache(1)
def get_container() -> Container:
    container = init_container()
    return container


@lru_cache(1)
def init_logger() -> logging.Logger:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )


def init_container() -> Container:
    container = Container()
    engine = create_engine()
    session_factory = create_session_factory(engine)

    container.register("lifespan_engine", instance=engine)

    def get_session() -> AsyncSession:
        session = session_factory()
        return session

    container.register(
        async_sessionmaker, instance=session_factory, scope=Scope.singleton
    )

    container.register(AsyncSession, factory=get_session, scope=Scope.transient)
    container.register(
        BaseTransactionManager, TransactionManager, scope=Scope.transient
    )
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
    container.register(ChangeUserSubscription, scope=Scope.transient)
    container.register(CreateUser, scope=Scope.transient)
    container.register(DeleteUser, scope=Scope.transient)
    container.register(GetAllUsers, scope=Scope.transient)
    container.register(GetUserByTelegramId, scope=Scope.transient)
    container.register(GetUserRequests, scope=Scope.transient)
    container.register(GetUserSubscriptions, scope=Scope.transient)
    container.register(UpdateUserRequests, scope=Scope.transient)

    container.register(SubscriptionService, scope=Scope.transient)
    container.register(NeuralNetworkService, scope=Scope.transient)

    return container
