from dataclasses import dataclass

from application.contracts.subscriptions.get_subscription_response import (
    GetSubscriptionResponse,
    ModelSubscriptionResponse,
)
from domain.exceptions.subscription import SubscriptionNotFoundException
from domain.neural_networks.repository import (
    BaseNeuralNetworkRepository,
    BaseNeuralNetworkSubscriptionRepository,
)
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription


@dataclass
class GetAllSubscriptions:
    subscription_repository: BaseSubscriptionRepository

    async def __call__(self) -> list[Subscription]:
        return await self.subscription_repository.get_all()


@dataclass
class GetSubscriptionByName:
    subscription_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository
    neural_network_subscriptoin_repository: BaseNeuralNetworkSubscriptionRepository

    async def __call__(self, name: str) -> GetSubscriptionResponse:
        subscription = await self.subscription_repository.get_by_name(name)
        if not subscription:
            raise SubscriptionNotFoundException

        neural_networks = await self.neural_network_subscriptoin_repository.get_all_by_subscription_name(
            subscription.name
        )

        models = [ModelSubscriptionResponse(item.neural_network_name, item.requests) for item in neural_networks]
        return GetSubscriptionResponse(name=subscription.name, models=models)
