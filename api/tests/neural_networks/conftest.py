import pytest

from src.domain.neural_networks.repository import BaseNeuralNetworkRepository
from src.domain.subscriptions.repository import BaseSubscriptionRepository
from src.domain.subscriptions.subscription import Subscription

# @pytest.fixture(scope="function")
# def neural_network_repository(container):
#     neural_network_repository = container.resolve(BaseNeuralNetworkRepository)
#     yield neural_network_repository


# @pytest.fixture(scope="function")
# def subscription_repository(container):
#     subscription_repository = container.resolve(BaseSubscriptionRepository)
#     yield subscription_repository
