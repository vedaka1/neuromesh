import uuid
from dataclasses import dataclass
from datetime import datetime

from application.common.transaction import ICommiter
from domain.exceptions.subscription import SubscriptionExpiredException, SubscriptionNotFoundException
from domain.exceptions.user import UserAlreadySubscribedException, UserNotFoundException
from domain.neural_networks.repository import BaseNeuralNetworkSubscriptionRepository
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import (
    BaseUserRepository,
    BaseUserRequestRepository,
    BaseUserSubscriptionRepository,
)
from domain.users.user import UserRequest, UserSubscription


@dataclass
class UpdateUserRequests:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    commiter: ICommiter

    async def __call__(self, user_id: uuid.UUID, model_name: str, amount: int) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException

        await self.user_requests_repository.update_user_requests(user_id, model_name, amount)
        await self.commiter.commit()


@dataclass
class UpdateUserSubscription:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    user_subscriptions_repository: BaseUserSubscriptionRepository
    subscriptions_repository: BaseSubscriptionRepository
    neural_network_subscriptions_repository: BaseNeuralNetworkSubscriptionRepository
    commiter: ICommiter

    async def __call__(self, user_id: uuid.UUID, subscription_name: str) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException

        subscription = await self.subscriptions_repository.get_by_name(subscription_name)
        if not subscription:
            raise SubscriptionNotFoundException

        current_user_subscription = await self.user_subscriptions_repository.get_active_by_user_id(user.id)
        if current_user_subscription:
            raise UserAlreadySubscribedException

        user_subscription = UserSubscription.create(
            user_id=user.id,
            subscription_name=subscription.name,
            expires_in=30,
        )
        if subscription.name != 'Free':
            await self.user_subscriptions_repository.create(user_subscription)
        await self.user_repository.update_subscription(user.id, subscription_name)
        await self.user_requests_repository.delete_user_requests(user.id)
        neural_networks = await self.neural_network_subscriptions_repository.get_all_by_subscription_name(
            subscription.name
        )
        if neural_networks:
            for neural_network in neural_networks:
                user_request = UserRequest.create(
                    user_id=user.id,
                    neural_network_name=neural_network.neural_network_name,
                    amount=neural_network.requests,
                )
                await self.user_requests_repository.create(user_request)
        await self.commiter.commit()


@dataclass
class CheckUserSubscription:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    user_subscriptions_repository: BaseUserSubscriptionRepository
    subscriptions_repository: BaseSubscriptionRepository
    neural_network_subscriptions_repository: BaseNeuralNetworkSubscriptionRepository
    commiter: ICommiter

    async def __call__(self, user_id: uuid.UUID) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException

        if user.current_subscription != 'Free':
            current_user_subscription = await self.user_subscriptions_repository.get_active_by_user_id(user.id)
            if not current_user_subscription:
                raise SubscriptionExpiredException

            if datetime.now() >= current_user_subscription.expires_in:
                await self.user_subscriptions_repository.update(current_user_subscription.id)
                await self.user_repository.update_subscription(user.id, 'Free')
                await self.user_requests_repository.delete_user_requests(user.id)
                neural_networks = await self.neural_network_subscriptions_repository.get_all_by_subscription_name(
                    'Free'
                )
                for neural_network in neural_networks:
                    user_request = UserRequest.create(
                        user_id=user.id,
                        neural_network_name=neural_network.neural_network_name,
                        amount=neural_network.requests,
                    )
                    await self.user_requests_repository.create(user_request)
                await self.commiter.commit()
                raise SubscriptionExpiredException
