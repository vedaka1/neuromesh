from dataclasses import dataclass

from application.common.transaction import ICommiter
from domain.exceptions.model import ModelNotFoundException
from domain.neural_networks.repository import BaseNeuralNetworkRepository


@dataclass
class DeleteNeuralNetwork:
    neural_network_repository: BaseNeuralNetworkRepository
    commiter: ICommiter

    async def __call__(self, model_name: str) -> None:
        model = await self.neural_network_repository.get_by_name(model_name)
        if not model:
            raise ModelNotFoundException

        await self.neural_network_repository.delete(model.name)
        await self.commiter.commit()

        return None
