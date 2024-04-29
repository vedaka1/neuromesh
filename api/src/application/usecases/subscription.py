from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.contracts.subscriptions.create_subscription_request import (
    CreateSubscriptionRequest,
)
from application.contracts.subscriptions.get_subscription_response import (
    GetSubscriptionResponse,
)
from domain.neural_networks.model import Model, ModelSubscription
from domain.neural_networks.repository import (
    BaseNeuralNetworkRepository,
    BaseNeuralNetworkSubscriptionRepository,
)
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription


@dataclass
class SubscriptionService:
    subscription_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository
    neural_network_subscriptoin_repository: BaseNeuralNetworkSubscriptionRepository

    async def create(self, request: CreateSubscriptionRequest) -> Subscription:
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

        neural_networks = await self.neural_network_subscriptoin_repository.get_all_by_subscription_id(
            subscription.id
        )
        models = []
        for neural_network in neural_networks:
            neural_network = await self.neural_network_repository.get_by_id(
                neural_network.neural_network_id
            )
            models.append(neural_network)

        return GetSubscriptionResponse(
            id=subscription.id,
            name=subscription.name,
            models=models,
        )

    async def get_all(self) -> list[Subscription]:
        subscriptions = await self.subscription_repository.get_all()

        return subscriptions

    async def add_model_to_subscription(
        self, subscription_name: str, model_name: str, requests: int
    ) -> ModelSubscription:
        subscription = await self.subscription_repository.get_by_name(subscription_name)

        if subscription is None:
            raise HTTPException(status_code=404, detail="Subscription not found")

        model = await self.neural_network_repository.get_by_name(model_name)

        if model is None:
            raise HTTPException(status_code=404, detail="Model not found")

        subscription_models = await self.neural_network_subscriptoin_repository.get_all_by_subscription_id(
            subscription.id
        )

        for subscription_model in subscription_models:
            if subscription_model.neural_network_id == model.id:
                raise HTTPException(
                    status_code=400, detail="Model already added to subscription"
                )

        model_subscription = ModelSubscription.create(
            model_id=model.id, subscription_id=subscription.id, requests=requests
        )

        await self.neural_network_subscriptoin_repository.create(model_subscription)

        return model_subscription
