from functools import lru_cache

from punq import Container, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker

from application.usecases.neural_network import NeuralNetworkService
from application.usecases.subscription import SubscriptionService
from application.usecases.user import UserService
from domain.neural_networks.repository import BaseNeuralNetworkRepository
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import (
    BaseUserRepository,
    BaseUserRequestRepository,
    BaseUserSubscriptionRepository,
)
from infrastructure.persistence.main import create_engine, create_session_factory
from infrastructure.persistence.repositories import (
    NeuralNetworkRepository,
    SubscriptionRepository,
    UserRepository,
    UserRequestRepository,
    UserSubscriptionRepository,
)


@lru_cache(1)
def get_container() -> Container:
    container = init_container()
    return container


def init_container() -> Container:
    container = Container()
    engine = create_engine()
    session_factory = create_session_factory(engine)
    container.register(
        async_sessionmaker, instance=session_factory, scope=Scope.singleton
    )

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
    container.register(UserService, scope=Scope.transient)
    container.register(SubscriptionService, scope=Scope.transient)
    container.register(NeuralNetworkService, scope=Scope.transient)
    return container
