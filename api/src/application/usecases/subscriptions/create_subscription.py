from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.common.transaction import BaseTransactionManager
from application.contracts.subscriptions.create_subscription_request import (
    CreateSubscriptionRequest,
)
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription


@dataclass
class CreateSubscription:
    subscription_repository: BaseSubscriptionRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, request: CreateSubscriptionRequest) -> Subscription:
        subscription_exist = await self.subscription_repository.get_by_name(
            request.name
        )

        if subscription_exist:
            raise HTTPException(status_code=400, detail="Subscription already exist")

        subscription = Subscription.create(name=request.name)
        await self.subscription_repository.create(subscription)

        await self.transaction_manager.commit()

        return subscription
