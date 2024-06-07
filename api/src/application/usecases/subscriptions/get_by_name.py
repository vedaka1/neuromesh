from dataclasses import dataclass

from application.contracts.subscriptions.get_subscription_response import (
    GetSubscriptionResponse,
)
from domain.neural_networks.repository import (
    BaseNeuralNetworkRepository,
    BaseNeuralNetworkSubscriptionRepository,
)
from domain.subscriptions.repository import BaseSubscriptionRepository
from fastapi.exceptions import HTTPException


@dataclass
class GetSubscriptionByName:
    subscription_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository
    neural_network_subscriptoin_repository: BaseNeuralNetworkSubscriptionRepository

    async def __call__(self, name: str) -> GetSubscriptionResponse:
        subscription = await self.subscription_repository.get_by_name(name)

        if subscription is None:
            raise HTTPException(status_code=404, detail="Subscription not found")

        neural_networks = await self.neural_network_subscriptoin_repository.get_all_by_subscription_name(
            subscription.name
        )
        models = []
        for neural_network in neural_networks:
            neural_network = await self.neural_network_repository.get_by_name(
                neural_network.neural_network_name
            )
            models.append(neural_network)

        return GetSubscriptionResponse(
            name=subscription.name,
            models=models,
        )
