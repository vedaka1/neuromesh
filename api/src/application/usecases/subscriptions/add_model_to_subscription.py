from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.common.transaction import BaseTransactionManager
from application.contracts.subscriptions.create_subscription_request import (
    CreateSubscriptionRequest,
)
from application.contracts.subscriptions.get_subscription_response import (
    GetSubscriptionResponse,
)
from domain.neural_networks.repository import (
    BaseNeuralNetworkRepository,
    BaseNeuralNetworkSubscriptionRepository,
)
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription


@dataclass
class AddModelToSubscription:
    subscription_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository
    neural_network_subscriptoin_repository: BaseNeuralNetworkSubscriptionRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, request: CreateSubscriptionRequest) -> Subscription:
        subscription_exist = await self.subscription_repository.get_by_name(
            request.name
        )

        if subscription_exist:
            raise HTTPException(status_code=400, detail="Subscription already exist")

        subscription = Subscription.create(name=request.name)
        await self.subscription_repository.create(subscription)

        return subscription

    async def get_by_name(self, name: str) -> GetSubscriptionResponse:
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

        await self.transaction_manager.commit()
        await self.transaction_manager.close()

        return GetSubscriptionResponse(
            name=subscription.name,
            models=models,
        )
