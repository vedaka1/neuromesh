from dataclasses import dataclass

from application.common.transaction import BaseTransactionManager
from domain.exceptions.subscription import *
from domain.subscriptions.repository import BaseSubscriptionRepository


@dataclass
class DeleteSubscription:
    subscription_repository: BaseSubscriptionRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, subscription_name: str) -> None:
        subscription = await self.subscription_repository.get_by_name(subscription_name)
        if subscription is None:
            raise SubscriptionNotFoundException
        await self.subscription_repository.delete(subscription.name)
        await self.transaction_manager.commit()
        return None
