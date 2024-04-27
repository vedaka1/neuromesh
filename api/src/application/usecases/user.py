from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.contracts.users.get_user_response import GetUserResponse
from application.contracts.users.register_request import RegisterRequest
from domain.neural_networks.repository import BaseNeuralNetworkRepository
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import BaseUserRepository, BaseUserRequestRepository
from domain.users.user import UserDB, UserRequest


@dataclass
class UserService:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    subscriptions_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository

    async def create(self, request: RegisterRequest) -> UserDB:
        user_exists = await self.user_repository.get_by_telegram_id(request.telegram_id)

        if user_exists:
            raise HTTPException(status_code=400, detail="User already exists")

        user = UserDB.create(telegram_id=request.telegram_id, username=request.username)
        await self.user_repository.create(user)

        subscription = await self.subscriptions_repository.get_by_name("free")
        neural_networks = (
            await self.neural_network_repository.get_all_by_subscription_id(
                subscription.id
            )
        )

        if neural_networks:
            for neural_network in neural_networks:
                user_request = UserRequest.create(
                    user_id=user.id,
                    neural_network_id=neural_network.id,
                    amount=neural_network.requests_amount,
                )
                await self.user_requests_repository.create(user_request)

        return user

    async def get_user_by_telegram_id(self, user_id: int) -> UserDB:
        user = await self.user_repository.get_by_telegram_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def get_all(self) -> list[UserDB]:
        return await self.user_repository.get_all()

    async def delete_by_id(self, user_id: int) -> None:
        await self.user_repository.delete(user_id)

    async def get_user_requests(self, user_id: int) -> list[UserRequest]:
        requests = await self.user_requests_repository.get_all_by_user_id(user_id)

        return requests
