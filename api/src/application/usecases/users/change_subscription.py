import uuid
from dataclasses import dataclass
from datetime import timedelta

from fastapi import HTTPException

from application.common.transaction import BaseTransactionManager
from domain.neural_networks.repository import BaseNeuralNetworkSubscriptionRepository
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.users.repository import (
    BaseUserRepository,
    BaseUserRequestRepository,
    BaseUserSubscriptionRepository,
)
from domain.users.user import UserRequest, UserSubscription


@dataclass
class ChangeUserSubscription:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    user_subscriptions_repository: BaseUserSubscriptionRepository
    subscriptions_repository: BaseSubscriptionRepository
    neural_network_subscriptions_repository: BaseNeuralNetworkSubscriptionRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, user_id: uuid.UUID, subscription_name: str) -> None:
        if subscription_name == "Free":
            await self.user_repository.update_subscription(user_id, None)
            return None

        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        subscription = await self.subscriptions_repository.get_by_name(
            subscription_name
        )
        if subscription is None:
            raise HTTPException(status_code=404, detail="Subscription not found")
        neural_networks = await self.neural_network_subscriptions_repository.get_all_by_subscription_name(
            subscription.name
        )
        # if user.current_subscription:
        #     raise HTTPException(status_code=400, detail="User already subscribed")

        user_subscription = UserSubscription.create(
            user_id=user.id,
            subscription_name=subscription.name,
            expires_in=timedelta(days=30).total_seconds(),
        )
        await self.user_subscriptions_repository.create(user_subscription)
        await self.user_repository.update_subscription(user.id, subscription_name)

        await self.user_requests_repository.delete_user_requests(user.id)
        if neural_networks:
            for neural_network in neural_networks:
                user_request = UserRequest.create(
                    user_id=user.id,
                    neural_network_name=neural_network.neural_network_name,
                    amount=neural_network.requests,
                )
                await self.user_requests_repository.create(user_request)

        await self.transaction_manager.commit()
        await self.transaction_manager.close()
