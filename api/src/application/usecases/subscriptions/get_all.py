from dataclasses import dataclass

from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription


@dataclass
class GetAllSubscriptions:
    subscription_repository: BaseSubscriptionRepository

    async def __call__(self) -> list[Subscription]:
        subscriptions = await self.subscription_repository.get_all()
        return subscriptions
