import pytest
from dishka import AsyncContainer

from domain.neural_networks.model import Model
from domain.neural_networks.repository import BaseNeuralNetworkRepository

pytestmark = pytest.mark.asyncio(scope="session")


class TestNeuralNetworkRepository:

    async def test_create_neural_network(self, container: AsyncContainer):
        async with container() as di_container:
            neural_network_repository = await di_container.get(
                BaseNeuralNetworkRepository
            )
            # Create model
            model = Model.create("test_neuro")
            await neural_network_repository.create(model)
            # Check it
            result = await neural_network_repository.get_by_name(model.name)
            assert result.name == model.name
            # Delete model
            await neural_network_repository.delete(model.name)

    async def test_delete_neural_network(self, container: AsyncContainer):
        async with container() as di_container:
            neural_network_repository = await di_container.get(
                BaseNeuralNetworkRepository
            )
            # Create model
            model = Model.create("test_neuro")
            await neural_network_repository.create(model)
            # Delete model
            await neural_network_repository.delete(model.name)
            # Check it
            result = await neural_network_repository.get_by_name(model.name)
            assert result is None

    async def test_get_neural_network_by_id(self, container: AsyncContainer):
        async with container() as di_container:
            neural_network_repository = await di_container.get(
                BaseNeuralNetworkRepository
            )
            # Create model
            model = Model.create("test_neuro")
            await neural_network_repository.create(model)
            # Check it and get it
            result = await neural_network_repository.get_by_name(model.name)
            assert str(result.name) == str(model.name)
            # Delete model
            await neural_network_repository.delete(model.name)

    async def test_get_all_neural_networks(self, container: AsyncContainer):
        async with container() as di_container:
            neural_network_repository = await di_container.get(
                BaseNeuralNetworkRepository
            )
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
                await neural_network_repository.delete(model.name)

            result = await neural_network_repository.get_all()
            assert len(result) == 0
