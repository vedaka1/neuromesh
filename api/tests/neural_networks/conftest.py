import pytest

from src.domain.neural_networks.repository import BaseNeuralNetworkRepository
from src.domain.subscriptions.repository import BaseSubscriptionRepository
from src.domain.subscriptions.subscription import Subscription


@pytest.fixture(scope="function")
def neural_network_repository(container):
    neural_network_repository = container.resolve(BaseNeuralNetworkRepository)
    yield neural_network_repository


@pytest.fixture(scope="session")
async def mock_subscription(container):
    mock_subscription_repository = container.resolve(BaseSubscriptionRepository)
    subscription = Subscription.create("mock_sub", 200)
    await mock_subscription_repository.create(subscription)
    yield subscription
    await mock_subscription_repository.delete(subscription.id)
