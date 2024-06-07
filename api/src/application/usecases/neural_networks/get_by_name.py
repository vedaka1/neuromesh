from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.common.transaction import BaseTransactionManager
from domain.neural_networks.model import Model
from domain.neural_networks.repository import BaseNeuralNetworkRepository


@dataclass
class GetNeuralNetworkByName:
    neural_network_repository: BaseNeuralNetworkRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, name: str) -> Model:
        model = await self.neural_network_repository.get_by_name(name)

        if model is None:
            raise HTTPException(status_code=404, detail="Model not found")

        await self.transaction_manager.close()

        return model
