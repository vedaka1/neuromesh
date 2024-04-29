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
    ):
        # Create model
        model = Model.create("test_neuro")
        await neural_network_repository.create(model)
        # Check it
        result = await neural_network_repository.get_by_id(model.id)
        assert result.id == model.id
        assert result.name == model.name
        # Delete model
        await neural_network_repository.delete(model.id)

    async def test_delete_neural_network(
        self,
        neural_network_repository: NeuralNetworkRepository,
    ):
        # Create model
        model = Model.create("test_neuro")
        await neural_network_repository.create(model)
        # Delete model
        await neural_network_repository.delete(model.id)
        # Check it
        result = await neural_network_repository.get_by_id(model.id)
        assert result is None

    async def test_get_neural_network_by_id(
        self,
        neural_network_repository: NeuralNetworkRepository,
    ):
        # Create model
        model = Model.create("test_neuro")
        await neural_network_repository.create(model)
        # Check it and get it
        result = await neural_network_repository.get_by_id(model.id)
        assert str(result.id) == str(model.id)
        # Delete model
        await neural_network_repository.delete(model.id)

    async def test_get_all_neural_networks(
        self,
        neural_network_repository: NeuralNetworkRepository,
    ):
        # Create neural_networks
        count = 2
        for i in range(count):
            model = Model.create(f"test_neuro{i}")
            await neural_network_repository.create(model)
        # Check neural_networks
        result = await neural_network_repository.get_all()
        assert len(result) == count
        # Delete neural_networks
        for model in result:
            await neural_network_repository.delete(model.id)

        result = await neural_network_repository.get_all()
        assert len(result) == 0
