from dataclasses import dataclass

from fastapi import HTTPException

from application.common.transaction import BaseTransactionManager
from application.contracts.users.register_request import RegisterRequest
from domain.exceptions.user import *
from domain.neural_networks.repository import BaseNeuralNetworkSubscriptionRepository
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import BaseUserRepository, BaseUserRequestRepository
from domain.users.user import User, UserDB, UserRequest


@dataclass
class CreateUser:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    subscriptions_repository: BaseSubscriptionRepository
    neural_network_subscriptions_repository: BaseNeuralNetworkSubscriptionRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, request: RegisterRequest) -> UserDB:
        user_exists = await self.user_repository.get_by_telegram_id(request.telegram_id)
        if user_exists:
            raise UserAlreadyExistsException
        user = UserDB.create(telegram_id=request.telegram_id, username=request.username)
        await self.user_repository.create(user)

        subscription = await self.subscriptions_repository.get_by_name("Free")
        neural_networks = await self.neural_network_subscriptions_repository.get_all_by_subscription_name(
            subscription.name
        )
        if neural_networks:
            for neural_network in neural_networks:
                user_request = UserRequest.create(
                    user_id=user.id,
                    neural_network_name=neural_network.neural_network_name,
                    amount=30,
                )
                await self.user_requests_repository.create(user_request)

        await self.transaction_manager.commit()
        return user
