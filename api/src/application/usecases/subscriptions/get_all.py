from dataclasses import dataclass

from application.common.transaction import BaseTransactionManager
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription


@dataclass
class GetAllSubscriptions:
    subscription_repository: BaseSubscriptionRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self) -> list[Subscription]:
        subscriptions = await self.subscription_repository.get_all()

        await self.transaction_manager.close()
        return subscriptions
