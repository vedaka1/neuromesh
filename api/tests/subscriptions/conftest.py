import pytest

from src.domain.subscriptions.repository import BaseSubscriptionRepository


@pytest.fixture(scope="function")
def subscription_repository(container):
    subscription_repository = container.resolve(BaseSubscriptionRepository)
    yield subscription_repository
