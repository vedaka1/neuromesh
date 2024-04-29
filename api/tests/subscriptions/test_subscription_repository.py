import uuid

import pytest

from src.domain.subscriptions.subscription import Subscription
from src.infrastructure.persistence.repositories.subscription import (
    SubscriptionRepository,
)


@pytest.mark.asyncio
class TestSubscriptionRepository:
    async def test_create_subscription(
        self, subscription_repository: SubscriptionRepository
    ):
        # Create subscription
        subscription = Subscription.create("test_sub")
        await subscription_repository.create(subscription)
        # Check it
        result = await subscription_repository.get_by_id(subscription.id)
        assert result.id == subscription.id
        assert result.name == subscription.name
        # Delete subscription
        await subscription_repository.delete(subscription.id)

    async def test_delete_subscription(
        self, subscription_repository: SubscriptionRepository
    ):
        # Create subscription
        subscription = Subscription.create("test_sub")
        await subscription_repository.create(subscription)
        # Delete subscription
        await subscription_repository.delete(subscription.id)
        # Check it
        result = await subscription_repository.get_by_id(subscription.id)
        assert result is None

    async def test_get_subscription_by_id(
        self, subscription_repository: SubscriptionRepository
    ):
        # Create subscription
        subscription = Subscription.create("test_sub")
        await subscription_repository.create(subscription)
        # Check it and get it
        result = await subscription_repository.get_by_id(subscription.id)
        assert str(result.id) == str(subscription.id)
        # Delete subscription
        await subscription_repository.delete(subscription.id)

    async def test_get_all_subscriptions(
        self, subscription_repository: SubscriptionRepository
    ):
        # Create subscriptions
        count = 2
        for i in range(count):
            subscription = Subscription.create(f"test_sub{i}")
            await subscription_repository.create(subscription)
        # Check subscriptions
        result = await subscription_repository.get_all()
        assert len(result) == count
        # Delete subscriptions
        for subscription in result:
            await subscription_repository.delete(subscription.id)

        result = await subscription_repository.get_all()
        assert len(result) == 0

    async def test_update_subscription_validity_period(
        self, subscription_repository: SubscriptionRepository
    ):
        # Create subscription
        subscription = Subscription.create("test_sub")
        await subscription_repository.create(subscription)
        result = await subscription_repository.get_by_id(subscription.id)
        # Check it and get it
        assert result.name == "test_sub"
        await subscription_repository.update(subscription.id, "gpt")
        # Update validity_period
        result = await subscription_repository.get_by_id(subscription.id)
        # Check validity_period
        assert result.name == "gpt"
        await subscription_repository.delete(subscription.id)  # Delete subscription
