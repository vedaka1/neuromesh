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

    @classmethod
    async def create_user(cls, request: RegisterRequest) -> GetUserResponse:
        user_exists = await cls.user_repository.get_by_telegram_id(request.telegram_id)

        if user_exists:
            raise HTTPException(status_code=400, detail="User already exists")

        user = UserDB.create(telegram_id=request.telegram_id, username=request.username)
        await cls.user_repository.create(user)

        subscription = await cls.subscriptions_repository.get_by_name("free")
        neural_networks = (
            await cls.neural_network_repository.get_all_by_subscription_id(
                subscription.id
            )
        )

        for neural_network in neural_networks:
            user_request = UserRequest.create(
                user_id=user.id,
                neural_network_id=neural_network.id,
                amount=neural_network.requests_amount,
            )
            await cls.user_requests_repository.create(user_request)

        return GetUserResponse(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
        )

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> GetUserResponse:
        user = await cls.user_repository.get_by_telegram_id(user_id)

        return GetUserResponse(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
        )
