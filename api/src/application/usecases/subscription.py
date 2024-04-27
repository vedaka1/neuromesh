from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.contracts.subscriptions.create_subscription_request import (
    CreateSubscriptionRequest,
)
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription


@dataclass
class SubscriptionService:
    subscription_repository: BaseSubscriptionRepository

    async def create(self, request: CreateSubscriptionRequest) -> Subscription:
        subscription_exist = await self.subscription_repository.get_by_name(
            request.name
        )

        if subscription_exist:
            raise HTTPException(status_code=400, detail="Subscription already exist")

        subscription = Subscription.create(
            name=request.name, validity_period=request.validity_period
        )
        await self.subscription_repository.create(subscription)

        return subscription

    async def get_by_name(self, name: str) -> Subscription:
        subscription = await self.subscription_repository.get_by_name(name)

        if subscription is None:
            raise HTTPException(status_code=404, detail="Subscription not found")

        return subscription

    async def get_all(self) -> list[Subscription]:
        subscriptions = await self.subscription_repository.get_all()

        return subscriptions
