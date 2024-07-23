import uuid
from dataclasses import dataclass

from fastapi import HTTPException

from application.contracts.users.get_user_requests import GetUserRequestsResponse
from application.contracts.users.get_user_response import GetUserResponse
from application.contracts.users.get_user_subscriptions_response import (
    GetUserSubscriptionResponse,
)
from domain.exceptions.user import *
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import (
    BaseUserRepository,
    BaseUserRequestRepository,
    BaseUserSubscriptionRepository,
)
from domain.users.user import UserDB, UserRequest, UserSubscription


@dataclass
class GetAllUsers:
    user_repository: BaseUserRepository

    async def __call__(self) -> list[UserDB]:
        result = await self.user_repository.get_all()
        return result


@dataclass
class GetUserByTelegramId:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    user_subscriptions_repository: BaseUserSubscriptionRepository

    async def __call__(self, user_id: int) -> GetUserResponse:
        user = await self.user_repository.get_by_telegram_id(user_id)
        if user is None:
            raise UserNotFoundException

        subscription = await self.user_subscriptions_repository.get_active_by_user_id(
            user.id
        )
        requests = await self.user_requests_repository.get_all_by_user_id(user.id)

        return GetUserResponse(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
            subscription=(
                GetUserSubscriptionResponse(
                    subscription_name=subscription.subscription_name,
                    created_at=subscription.created_at,
                    expires_in=subscription.expires_in,
                )
                if subscription
                else GetUserSubscriptionResponse(
                    subscription_name="Free",
                    created_at=None,
                    expires_in=None,
                )
            ),
            requests=[
                GetUserRequestsResponse(request.neural_network_name, request.amount)
                for request in requests
            ],
        )


@dataclass
class GetUserRequests:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository

    async def __call__(self, user_id: uuid.UUID) -> list[GetUserRequestsResponse]:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException
        requests = await self.user_requests_repository.get_all_by_user_id(user_id)
        return [
            GetUserRequestsResponse(request.neural_network_name, request.amount)
            for request in requests
        ]


@dataclass
class GetUserSubscription:
    user_repository: BaseUserRepository
    user_subscriptions_repository: BaseUserSubscriptionRepository

    async def __call__(self, user_id: uuid.UUID) -> GetUserSubscriptionResponse:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException
        subscription = await self.user_subscriptions_repository.get_active_by_user_id(
            user_id
        )

        return (
            GetUserSubscriptionResponse(
                subscription_name=subscription.subscription_name,
                created_at=subscription.created_at,
                expires_in=subscription.expires_in,
            )
            if subscription
            else GetUserSubscriptionResponse(
                subscription_name="Free",
                created_at=None,
                expires_in=None,
            )
        )


@dataclass
class GetUserSubscriptions:
    user_repository: BaseUserRepository
    user_subscriptions_repository: BaseUserSubscriptionRepository

    async def __call__(self, user_id: uuid.UUID) -> list[GetUserSubscriptionResponse]:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException
        subscriptions = await self.user_subscriptions_repository.get_by_user_id(user_id)

        return [
            GetUserSubscriptionResponse(
                subscription_name=subscription.subscription_name,
                created_at=subscription.created_at,
                expires_in=subscription.expires_in,
                is_expired=subscription.is_expired,
            )
            for subscription in subscriptions
        ]
