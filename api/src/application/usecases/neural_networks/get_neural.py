from dataclasses import dataclass

from domain.exceptions.model import ModelNotFoundException
from domain.neural_networks.model import Model
from domain.neural_networks.repository import BaseNeuralNetworkRepository


@dataclass
class GetAllNeuralNetworks:
    neural_network_repository: BaseNeuralNetworkRepository

    async def __call__(self) -> list[Model]:
        result = await self.neural_network_repository.get_all()
        return result


@dataclass
class GetNeuralNetworkByName:
    neural_network_repository: BaseNeuralNetworkRepository

    async def __call__(self, name: str) -> Model:
        model = await self.neural_network_repository.get_by_name(name)
        if not model:
            raise ModelNotFoundException

        return model
