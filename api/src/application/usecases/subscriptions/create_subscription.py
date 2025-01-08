from dataclasses import dataclass

from application.common.transaction import ICommiter
from application.contracts.subscriptions.create_subscription_request import (
    CreateSubscriptionRequest,
)
from domain.exceptions.subscription import SubscriptionAlreadyExistsException
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription


@dataclass
class CreateSubscription:
    subscription_repository: BaseSubscriptionRepository
    commiter: ICommiter

    async def __call__(self, request: CreateSubscriptionRequest) -> Subscription:
        subscription_exist = await self.subscription_repository.get_by_name(request.name)
        if subscription_exist:
            raise SubscriptionAlreadyExistsException

        subscription = Subscription.create(name=request.name)
        await self.subscription_repository.create(subscription)
        await self.commiter.commit()

        return subscription
