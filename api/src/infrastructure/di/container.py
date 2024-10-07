import logging
import logging.handlers
from functools import lru_cache
from multiprocessing import Queue
from typing import AsyncGenerator

import aiohttp
import logging_loki
import openai
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from application.common.tg_client import AsyncTGClient
from application.common.transaction import BaseTransactionManager
from application.usecases.neural_networks import *
from application.usecases.neural_networks.generate_image import GenerateImage
from application.usecases.subscriptions import *
from application.usecases.users import *
from domain.neural_networks.manager import BaseModelManager
from domain.neural_networks.model import BaseImageModel
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
from infrastructure.config import settings
from infrastructure.neural_networks.image_models.kadinsky import Kadinsky
from infrastructure.neural_networks.main import ModelManager
from infrastructure.neural_networks.text_models.chatgpt import ChatGPT
from infrastructure.neural_networks.text_models.gigachat import Gigachat
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
def init_logger() -> None:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    return None


@lru_cache(1)
def init_loki_logger(app_name: str = "app"):
    return logging_loki.LokiQueueHandler(
        Queue(-1),  # type: ignore
        url="http://loki:3100/loki/api/v1/push",
        tags={"application": app_name},
        version="1",
    )


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        return create_engine()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
        return create_session_factory(engine)

    @provide(scope=Scope.APP)
    def tg_client(self) -> AsyncTGClient:
        return AsyncTGClient(base_url=settings.tg.TG_API)

    @provide(scope=Scope.APP)
    async def aiohttp_session(self) -> AsyncGenerator[aiohttp.ClientSession, None]:
        session = aiohttp.ClientSession()
        yield session
        await session.close()

    @provide(scope=Scope.APP)
    def openai_client(self) -> openai.AsyncOpenAI:
        return openai.AsyncOpenAI(api_key=settings.chatgpt.API_KEY_CHATGPT)


class DatabaseConfigurationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_db_connection(
        self, session_factory: async_sessionmaker
    ) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = session_factory()
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


class ModelsProvider(Provider):
    scope = Scope.APP
    image_model = provide(Kadinsky, provides=BaseImageModel)
    chatgpt_model = provide(ChatGPT)
    gigachat_model = provide(Gigachat)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    change_user_subscription = provide(UpdateUserSubscription)
    create_user = provide(CreateUser)
    delete_user = provide(DeleteUser)
    get_all_users = provide(GetAllUsers)
    get_user_by_tg_id = provide(GetUserByTelegramId)
    get_user_requests = provide(GetUserRequests)
    get_user_subscription = provide(GetUserSubscription)
    get_user_subscriptions = provide(GetUserSubscriptions)
    update_user_requests = provide(UpdateUserRequests)

    create_subscription = provide(CreateSubscription)
    delete_subscription = provide(DeleteSubscription)
    add_model_to_subscription = provide(AddModelToSubscription)
    delete_model_from_subscription = provide(DeleteModelFromSubscription)
    get_all_subscriptions = provide(GetAllSubscriptions)
    get_subscription_by_name = provide(GetSubscriptionByName)

    create_neural_network = provide(CreateNeuralNetwork)
    delete_neural_network = provide(DeleteNeuralNetwork)
    generate_response = provide(GenerateResponse)
    get_all_neural_networks = provide(GetAllNeuralNetworks)
    get_neural_network_by_name = provide(GetNeuralNetworkByName)
    check_user_subscription = provide(CheckUserSubscription)
    generate_image = provide(GenerateImage)


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        DatabaseConfigurationProvider(),
        DatabaseAdaptersProvider(),
        UseCasesProvider(),
        ModelsProvider(),
    )
