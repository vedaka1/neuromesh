from dataclasses import dataclass

from fastapi import HTTPException

from application.common.transaction import BaseTransactionManager
from application.contracts.users.get_user_response import GetUserResponse
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import BaseUserRepository, BaseUserRequestRepository


@dataclass
class GetUserByTelegramId:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    subscriptions_repository: BaseSubscriptionRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, user_id: int) -> GetUserResponse:
        user = await self.user_repository.get_by_telegram_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        subscription = await self.subscriptions_repository.get_by_name(
            user.current_subscription
        )
        requests = await self.user_requests_repository.get_all_by_user_id(user.id)

        await self.transaction_manager.close()
        return GetUserResponse(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
            subscription=subscription,
            requests=requests,
        )
