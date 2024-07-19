from dataclasses import dataclass

from fastapi import HTTPException

from application.contracts.subscriptions.get_subscription_response import (
    GetSubscriptionResponse,
)
from domain.exceptions.subscription import *
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
        subscriptions = await self.subscription_repository.get_all()
        return subscriptions


@dataclass
class GetSubscriptionByName:
    subscription_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository
    neural_network_subscriptoin_repository: BaseNeuralNetworkSubscriptionRepository

    async def __call__(self, name: str) -> GetSubscriptionResponse:
        subscription = await self.subscription_repository.get_by_name(name)

        if subscription is None:
            raise SubscriptionNotFoundException

        neural_networks = await self.neural_network_subscriptoin_repository.get_all_by_subscription_name(
            subscription.name
        )
        models = []
        for neural_network in neural_networks:
            if not neural_network:
                raise ApplicationException
            model = await self.neural_network_repository.get_by_name(
                neural_network.neural_network_name
            )
            if model:
                models.append(model)

        return GetSubscriptionResponse(
            name=subscription.name,
            models=models,
        )
