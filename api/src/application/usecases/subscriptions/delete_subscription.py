from dataclasses import dataclass

from application.common.transaction import ICommiter
from domain.exceptions.subscription import SubscriptionNotFoundException
from domain.subscriptions.repository import BaseSubscriptionRepository


@dataclass
class DeleteSubscription:
    subscription_repository: BaseSubscriptionRepository
    commiter: ICommiter

    async def __call__(self, subscription_name: str) -> None:
        subscription = await self.subscription_repository.get_by_name(subscription_name)
        if subscription is None:
            raise SubscriptionNotFoundException

        await self.subscription_repository.delete(subscription.name)
        await self.commiter.commit()

        return None
