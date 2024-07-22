from dataclasses import dataclass

from application.common.transaction import BaseTransactionManager
from domain.exceptions.model import *
from domain.neural_networks.repository import BaseNeuralNetworkRepository


@dataclass
class DeleteNeuralNetwork:
    neural_network_repository: BaseNeuralNetworkRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, model_name: str) -> None:
        model = await self.neural_network_repository.get_by_name(model_name)
        if not model:
            raise ModelNotFoundException
        await self.neural_network_repository.delete(model.name)
        await self.transaction_manager.commit()
        return None
