from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.common.transaction import BaseTransactionManager
from application.contracts.neural_networks.create_neural_network_request import (
    CreateNeuralNetworkRequest,
)
from domain.exceptions.model import *
from domain.neural_networks.model import Model
from domain.neural_networks.repository import BaseNeuralNetworkRepository


@dataclass
class CreateNeuralNetwork:
    neural_network_repository: BaseNeuralNetworkRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, request: CreateNeuralNetworkRequest) -> Model:
        model_exist = await self.neural_network_repository.get_by_name(request.name)

        if model_exist:
            raise ModelAlreadyExistsException
        model = Model.create(name=request.name)
        await self.neural_network_repository.create(model)

        await self.transaction_manager.commit()

        return model
