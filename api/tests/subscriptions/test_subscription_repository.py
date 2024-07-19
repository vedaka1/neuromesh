import pytest
from dishka import AsyncContainer

from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription

pytestmark = pytest.mark.asyncio(scope="session")


class TestSubscriptionRepository:
    async def test_create_subscription(self, container: AsyncContainer):
        async with container() as di_container:
            subscription_repository = await di_container.get(BaseSubscriptionRepository)
            # Create subscription
            subscription = Subscription.create("test_sub")
            await subscription_repository.create(subscription)
            # Check it
            result = await subscription_repository.get_by_name(subscription.name)
            assert result.name == subscription.name
            # Delete subscription
            await subscription_repository.delete(subscription.name)

    async def test_delete_subscription(self, container: AsyncContainer):
        async with container() as di_container:
            subscription_repository = await di_container.get(BaseSubscriptionRepository)
            # Create subscription
            subscription = Subscription.create("test_sub")
            await subscription_repository.create(subscription)
            # Delete subscription
            await subscription_repository.delete(subscription.name)
            # Check it
            result = await subscription_repository.get_by_name(subscription.name)
            assert result is None

    async def test_get_subscription_by_id(self, container: AsyncContainer):
        async with container() as di_container:
            subscription_repository = await di_container.get(BaseSubscriptionRepository)
            # Create subscription
            subscription = Subscription.create("test_sub")
            await subscription_repository.create(subscription)
            # Check it and get it
            result = await subscription_repository.get_by_name(subscription.name)
            assert str(result.name) == str(subscription.name)
            # Delete subscription
            await subscription_repository.delete(subscription.name)

    async def test_get_all_subscriptions(self, container: AsyncContainer):
        async with container() as di_container:
            subscription_repository = await di_container.get(BaseSubscriptionRepository)
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
                await subscription_repository.delete(subscription.name)

        result = await subscription_repository.get_all()
        assert len(result) == 0
