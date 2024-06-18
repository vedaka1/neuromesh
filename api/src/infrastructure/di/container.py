import logging
from functools import lru_cache
from typing import AsyncGenerator

from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from application.common.transaction import BaseTransactionManager
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
def init_logger() -> logging.Logger:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        return create_engine()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
        return create_session_factory(engine)


class DatabaseConfigurationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_db_connection(
        self, session_factory: async_sessionmaker
    ) -> AsyncGenerator[AsyncSession, None]:
        session = session_factory()
        yield session
        await session.close()


class DatabaseAdaptersProvider(Provider):
    scope = Scope.REQUEST

    unit_of_work = provide(TransactionManager, provides=BaseTransactionManager)
    model_manager = provide(ModelManager, provides=BaseModelManager)
    user_repository = provide(UserRepository, provides=BaseUserRepository)
    user_request_repository = provide(
        UserRequestRepository, provides=BaseUserRequestRepository
    )
    user_subscription_repository = provide(
        UserSubscriptionRepository, provides=BaseUserSubscriptionRepository
    )
    neural_network_subscription_repository = provide(
        NeuralNetworkSubscriptionRepository,
        provides=BaseNeuralNetworkSubscriptionRepository,
    )
    neural_network_repository = provide(
        NeuralNetworkRepository, provides=BaseNeuralNetworkRepository
    )
    subscription_repository = provide(
        SubscriptionRepository, provides=BaseSubscriptionRepository
    )


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    change_user_subscription = provide(UpdateUserSubscription)
    create_user = provide(CreateUser)
    delete_user = provide(DeleteUser)
    get_all_users = provide(GetAllUsers)
    get_user_by_tg_id = provide(GetUserByTelegramId)
    get_user_requests = provide(GetUserRequests)
    get_user_subscriptions = provide(GetUserSubscriptions)
    update_user_requests = provide(UpdateUserRequests)

    create_subscription = provide(CreateSubscription)
    add_model_to_subscription = provide(AddModelToSubscription)
    get_all_subscriptions = provide(GetAllSubscriptions)
    get_subscription_by_name = provide(GetSubscriptionByName)

    create_neural_network = provide(CreateNeuralNetwork)
    generate_response = provide(GenerateResponse)
    get_all_neural_networks = provide(GetAllNeuralNetworks)
    get_neural_network_by_name = provide(GetNeuralNetworkByName)
    check_user_subscription = provide(CheckUserSubscription)


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        DatabaseConfigurationProvider(),
        DatabaseAdaptersProvider(),
        UseCasesProvider(),
    )
