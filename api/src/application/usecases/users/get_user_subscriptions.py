import uuid
from dataclasses import dataclass

from domain.users.repository import BaseUserRepository, BaseUserSubscriptionRepository
from domain.users.user import UserSubscription
from fastapi import HTTPException


@dataclass
class GetUserSubscriptions:
    user_repository: BaseUserRepository
    user_subscriptions_repository: BaseUserSubscriptionRepository

    async def __call__(self, user_id: uuid.UUID) -> list[UserSubscription]:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        subscriptions = await self.user_subscriptions_repository.get_by_user_id(user_id)

        return subscriptions
