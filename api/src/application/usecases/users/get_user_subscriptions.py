import uuid
from dataclasses import dataclass

from fastapi import HTTPException

from application.common.transaction import BaseTransactionManager
from domain.users.repository import BaseUserRepository, BaseUserSubscriptionRepository
from domain.users.user import UserSubscription


@dataclass
class GetUserSubscriptions:
    user_repository: BaseUserRepository
    user_subscriptions_repository: BaseUserSubscriptionRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, user_id: uuid.UUID) -> list[UserSubscription]:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        subscriptions = await self.user_subscriptions_repository.get_by_user_id(user_id)

        await self.transaction_manager.close()

        return subscriptions
