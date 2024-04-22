import uuid

import pytest

from src.domain.neural_networks.model import Model
from src.domain.subscriptions.subscription import Subscription
from src.infrastructure.persistence.repositories import (
    NeuralNetworkRepository,
    SubscriptionRepository,
)


@pytest.mark.asyncio
class TestNeuralNetworkRepository:
    async def test_create_neural_network(
        self,
        neural_network_repository: NeuralNetworkRepository,
        subscription_repository: SubscriptionRepository,
    ):
        mock_subscription = Subscription.create("mock_sub", 200)
        await subscription_repository.create(mock_subscription)
        # Create model
        model = Model.create(mock_subscription.id, "test_neuro", 200)
        await neural_network_repository.create(model)
        # Check it
        result = await neural_network_repository.get_by_id(model.id)
        assert result.id == model.id
        assert result.name == model.name
        assert result.requests_amount == model.requests_amount
        # Delete model
        await neural_network_repository.delete(model.id)
        await subscription_repository.delete(mock_subscription.id)

    async def test_delete_neural_network(
        self,
        neural_network_repository: NeuralNetworkRepository,
        subscription_repository: SubscriptionRepository,
    ):
        mock_subscription = Subscription.create("mock_sub", 200)
        await subscription_repository.create(mock_subscription)
        # Create model
        model = Model.create(mock_subscription.id, "test_neuro", 200)
        await neural_network_repository.create(model)
        # Delete model
        await neural_network_repository.delete(model.id)
        # Check it
        result = await neural_network_repository.get_by_id(model.id)
        assert result is None
        await subscription_repository.delete(mock_subscription.id)

    async def test_get_neural_network_by_id(
        self,
        neural_network_repository: NeuralNetworkRepository,
        subscription_repository: SubscriptionRepository,
    ):
        mock_subscription = Subscription.create("mock_sub", 200)
        await subscription_repository.create(mock_subscription)
        # Create model
        model = Model.create(mock_subscription.id, "test_neuro", 200)
        await neural_network_repository.create(model)
        # Check it and get it
        result = await neural_network_repository.get_by_id(model.id)
        assert str(result.id) == str(model.id)
        # Delete model
        await neural_network_repository.delete(model.id)
        await subscription_repository.delete(mock_subscription.id)

    async def test_get_all_neural_networks(
        self,
        neural_network_repository: NeuralNetworkRepository,
        subscription_repository: SubscriptionRepository,
    ):
        mock_subscription = Subscription.create("mock_sub", 200)
        await subscription_repository.create(mock_subscription)
        # Create neural_networks
        count = 2
        for i in range(count):
            model = Model.create(mock_subscription.id, f"test_neuro{i}", 200)
            await neural_network_repository.create(model)
        # Check neural_networks
        result = await neural_network_repository.get_all()
        assert len(result) == count
        # Delete neural_networks
        for model in result:
            await neural_network_repository.delete(model.id)

        result = await neural_network_repository.get_all()
        assert len(result) == 0
        await subscription_repository.delete(mock_subscription.id)

    async def test_update_neural_network_requests_amount(
        self,
        neural_network_repository: NeuralNetworkRepository,
        subscription_repository: SubscriptionRepository,
    ):
        mock_subscription = Subscription.create("mock_sub", 200)
        await subscription_repository.create(mock_subscription)
        # Create model
        model = Model.create(mock_subscription.id, "test_neuro", 200)
        await neural_network_repository.create(model)
        result = await neural_network_repository.get_by_id(model.id)
        # Check it and get it
        assert result.requests_amount == 200
        await neural_network_repository.update_requests_amount(model.id, 400)
        # Update requests_amount
        result = await neural_network_repository.get_by_id(model.id)
        # Check requests_amount
        assert result.requests_amount == 400
        await neural_network_repository.delete(model.id)  # Delete model
        await subscription_repository.delete(mock_subscription.id)
