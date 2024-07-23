from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.common.transaction import BaseTransactionManager
from domain.exceptions.model import *
from domain.exceptions.subscription import *
from domain.neural_networks.model import ModelSubscription
from domain.neural_networks.repository import (
    BaseNeuralNetworkRepository,
    BaseNeuralNetworkSubscriptionRepository,
)
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import BaseUserRepository, BaseUserRequestRepository
from domain.users.user import UserRequest


@dataclass
class AddModelToSubscription:
    subscription_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository
    neural_network_subscription_repository: BaseNeuralNetworkSubscriptionRepository
    users_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository

    transaction_manager: BaseTransactionManager

    async def __call__(
        self, subscription_name: str, model_name: str, requests: int
    ) -> ModelSubscription:
        subscription = await self.subscription_repository.get_by_name(subscription_name)
        if subscription is None:
            raise SubscriptionNotFoundException
        model = await self.neural_network_repository.get_by_name(model_name)
        if model is None:
            raise ModelNotFoundException
        subscription_models = await self.neural_network_subscription_repository.get_all_by_subscription_name(
            subscription.name
        )
        for subscription_model in subscription_models:
            if subscription_model.neural_network_name == model.name:
                raise ModelAlreadyInSubscriptionException
        model_subscription = ModelSubscription.create(
            model_name=model.name,
            subscription_name=subscription.name,
            requests=requests,
        )
        await self.neural_network_subscription_repository.create(model_subscription)
        users = await self.users_repository.get_all()
        for user in users:
            if user.current_subscription == subscription.name:
                user_request = UserRequest.create(
                    user_id=user.id,
                    neural_network_name=model.name,
                    amount=model_subscription.requests,
                )
                await self.user_requests_repository.create(user_request)
        await self.transaction_manager.commit()
        return model_subscription


@dataclass
class DeleteModelFromSubscription:
    subscription_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository
    neural_network_subscription_repository: BaseNeuralNetworkSubscriptionRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, subscription_name: str, model_name: str) -> None:
        subscription = await self.subscription_repository.get_by_name(subscription_name)
        if subscription is None:
            raise SubscriptionNotFoundException
        model = await self.neural_network_repository.get_by_name(model_name)
        if model is None:
            raise ModelNotFoundException
        subscription_model = await self.neural_network_subscription_repository.get_by_subscription_and_model_name(
            subscription_name=subscription_name, model_name=model_name
        )
        if not subscription_model:
            raise ModelNotFoundException
        await self.neural_network_subscription_repository.delete(subscription_model.id)
        await self.transaction_manager.commit()
        return None
