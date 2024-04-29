import uuid
from dataclasses import dataclass
from datetime import timedelta

from fastapi.exceptions import HTTPException

from application.contracts.users.get_user_response import GetUserResponse
from application.contracts.users.register_request import RegisterRequest
from domain.neural_networks.repository import (
    BaseNeuralNetworkRepository,
    BaseNeuralNetworkSubscriptionRepository,
)
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import (
    BaseUserRepository,
    BaseUserRequestRepository,
    BaseUserSubscriptionRepository,
)
from domain.users.user import UserDB, UserRequest, UserSubscription


@dataclass
class UserService:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    user_subscriptions_repository: BaseUserSubscriptionRepository
    subscriptions_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository
    neural_network_subscriptions_repository: BaseNeuralNetworkSubscriptionRepository

    async def create(self, request: RegisterRequest) -> UserDB:
        user_exists = await self.user_repository.get_by_telegram_id(request.telegram_id)
        if user_exists:
            raise HTTPException(status_code=400, detail="User already exists")
        user = UserDB.create(telegram_id=request.telegram_id, username=request.username)
        await self.user_repository.create(user)
        subscription = await self.subscriptions_repository.get_by_name("free")
        neural_networks = await self.neural_network_subscriptions_repository.get_all_by_subscription_id(
            subscription.id
        )
        if neural_networks:
            for neural_network in neural_networks:
                user_request = UserRequest.create(
                    user_id=user.id,
                    neural_network_id=neural_network.neural_network_id,
                    amount=30,
                )
                await self.user_requests_repository.create(user_request)
        return user

    async def get_user_by_telegram_id(self, user_id: int) -> UserDB:
        user = await self.user_repository.get_by_telegram_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user.current_subscription_id:
            subscription = await self.user_subscriptions_repository.get_by_id(
                user.current_subscription_id
            )
        return user

    async def get_all(self) -> list[UserDB]:
        return await self.user_repository.get_all()

    async def delete_by_id(self, user_id: int) -> None:
        await self.user_repository.delete(user_id)

    async def get_user_requests(self, user_id: uuid.UUID) -> list[UserRequest]:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        requests = await self.user_requests_repository.get_all_by_user_id(user_id)
        return requests

    async def update_user_requests(self, user_id: uuid.UUID, amount: int) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await self.user_requests_repository.update_user_requests(user_id, amount)

    async def change_subscription(
        self, user_id: uuid.UUID, subscription_name: uuid.UUID
    ) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        subscription = await self.subscriptions_repository.get_by_name(
            subscription_name
        )
        if subscription is None:
            raise HTTPException(status_code=404, detail="Subscription not found")
        neural_networks = await self.neural_network_subscriptions_repository.get_all_by_subscription_id(
            subscription.id
        )
        if user.current_subscription_id:
            raise HTTPException(status_code=400, detail="User already subscribed")

        user_subscription = UserSubscription.create(
            user_id=user.id,
            subscription_id=subscription.id,
            expires_in=timedelta(days=30).total_seconds(),
        )
        await self.user_subscriptions_repository.create(user_subscription)
        await self.user_repository.update_subscription(user.id, user_subscription.id)

        await self.user_requests_repository.delete_user_requests(user.id)
        if neural_networks:
            for neural_network in neural_networks:
                user_request = UserRequest.create(
                    user_id=user.id,
                    neural_network_id=neural_network.neural_network_id,
                    amount=30,
                )
                await self.user_requests_repository.create(user_request)

    async def get_user_subscriptions(
        self, user_id: uuid.UUID
    ) -> list[UserSubscription]:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        subscriptions = await self.user_subscriptions_repository.get_by_user_id(user_id)
        return subscriptions
