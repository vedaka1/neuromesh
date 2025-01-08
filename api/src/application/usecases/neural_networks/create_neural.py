from dataclasses import dataclass

from application.common.transaction import ICommiter
from application.contracts.neural_networks.create_neural_network_request import (
    CreateNeuralNetworkRequest,
)
from domain.exceptions.model import ModelAlreadyExistsException
from domain.neural_networks.model import Model
from domain.neural_networks.repository import BaseNeuralNetworkRepository


@dataclass
class CreateNeuralNetwork:
    neural_network_repository: BaseNeuralNetworkRepository
    commiter: ICommiter

    async def __call__(self, request: CreateNeuralNetworkRequest) -> Model:
        model_exist = await self.neural_network_repository.get_by_name(request.name)
        if model_exist:
            raise ModelAlreadyExistsException

        model = Model.create(name=request.name)

        await self.neural_network_repository.create(model)
        await self.commiter.commit()

        return model
