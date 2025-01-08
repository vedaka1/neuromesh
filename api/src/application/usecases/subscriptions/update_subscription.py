from dataclasses import dataclass

from application.common.transaction import ICommiter
from domain.exceptions.model import ModelAlreadyInSubscriptionException, ModelNotFoundException
from domain.exceptions.subscription import SubscriptionNotFoundException
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
    commiter: ICommiter

    async def __call__(self, subscription_name: str, model_name: str, requests: int) -> ModelSubscription:
        subscription = await self.subscription_repository.get_by_name(subscription_name)
        if not subscription:
            raise SubscriptionNotFoundException

        model = await self.neural_network_repository.get_by_name(model_name)
        if not model:
            raise ModelNotFoundException

        subscription_models = await self.neural_network_subscription_repository.get_all_by_subscription_name(
            subscription.name
        )
        for subscription_model in subscription_models:
            if subscription_model.neural_network_name == model.name:
                raise ModelAlreadyInSubscriptionException

        model_subscription = ModelSubscription.create(model.name, subscription.name, requests)
        await self.neural_network_subscription_repository.create(model_subscription)

        users = await self.users_repository.get_all(limit=None)
        for user in users:
            if user.current_subscription == subscription.name:
                user_request = UserRequest.create(
                    user_id=user.id,
                    neural_network_name=model.name,
                    amount=model_subscription.requests,
                )
                await self.user_requests_repository.create(user_request)
        await self.commiter.commit()
        return model_subscription


@dataclass
class DeleteModelFromSubscription:
    subscription_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository
    neural_network_subscription_repository: BaseNeuralNetworkSubscriptionRepository
    commiter: ICommiter

    async def __call__(self, subscription_name: str, model_name: str) -> None:
        subscription = await self.subscription_repository.get_by_name(subscription_name)
        if not subscription:
            raise SubscriptionNotFoundException

        model = await self.neural_network_repository.get_by_name(model_name)
        if not model:
            raise ModelNotFoundException

        subscription_model = await self.neural_network_subscription_repository.get_by_subscription_and_model_name(
            subscription_name=subscription_name, model_name=model_name
        )
        if not subscription_model:
            raise ModelNotFoundException

        await self.neural_network_subscription_repository.delete(subscription_model.id)
        await self.commiter.commit()

        return None
