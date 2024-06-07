from dataclasses import dataclass

from domain.neural_networks.model import Model
from domain.neural_networks.repository import BaseNeuralNetworkRepository
from fastapi.exceptions import HTTPException


@dataclass
class GetNeuralNetworkByName:
    neural_network_repository: BaseNeuralNetworkRepository

    async def __call__(self, name: str) -> Model:
        model = await self.neural_network_repository.get_by_name(name)

        if model is None:
            raise HTTPException(status_code=404, detail="Model not found")

        return model
