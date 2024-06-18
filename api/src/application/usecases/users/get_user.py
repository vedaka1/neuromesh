import uuid
from dataclasses import dataclass

from fastapi import HTTPException

from application.contracts.users.get_user_response import GetUserResponse
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import (
    BaseUserRepository,
    BaseUserRequestRepository,
    BaseUserSubscriptionRepository,
)
from domain.users.user import User, UserRequest, UserSubscription


@dataclass
class GetAllUsers:
    user_repository: BaseUserRepository

    async def __call__(self) -> list[User]:
        result = await self.user_repository.get_all()
        return result


@dataclass
class GetUserByTelegramId:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    subscriptions_repository: BaseSubscriptionRepository

    async def __call__(self, user_id: int) -> GetUserResponse:
        user = await self.user_repository.get_by_telegram_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        subscription = await self.subscriptions_repository.get_by_name(
            user.current_subscription
        )
        requests = await self.user_requests_repository.get_all_by_user_id(user.id)

        return GetUserResponse(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
            subscription=subscription,
            requests=requests,
        )


@dataclass
class GetUserRequests:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository

    async def __call__(self, user_id: uuid.UUID) -> list[UserRequest]:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        requests = await self.user_requests_repository.get_all_by_user_id(user_id)

        return requests


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
