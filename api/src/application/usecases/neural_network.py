import uuid
from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.contracts.neural_networks.create_neural_network_request import (
    CreateNeuralNetworkRequest,
)
from application.contracts.neural_networks.generate_response_request import (
    GenerateResponseRequest,
)
from domain.common.response import ModelResponse
from domain.neural_networks.manager import BaseModelManager
from domain.neural_networks.model import Model
from domain.neural_networks.repository import BaseNeuralNetworkRepository
from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription
from domain.users.repository import BaseUserRepository, BaseUserRequestRepository


@dataclass
class NeuralNetworkService:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository
    subscription_repository: BaseSubscriptionRepository
    neural_network_repository: BaseNeuralNetworkRepository
    model_manager: BaseModelManager

    async def create(self, request: CreateNeuralNetworkRequest) -> Model:
        model_exist = await self.neural_network_repository.get_by_name(request.name)

        if model_exist:
            raise HTTPException(
                status_code=400, detail="Neural network model already exist"
            )

        model = Model.create(
            name=request.name,
            subscription_id=request.subscription_id,
            requests_amount=request.requests_amount,
        )
        await self.neural_network_repository.create(model)

        return model

    async def get_by_name(self, name: str) -> Model:
        model = await self.neural_network_repository.get_by_name(name)

        if model is None:
            raise HTTPException(status_code=404, detail="Model not found")

        return model

    async def generate_response(
        self, request: GenerateResponseRequest
    ) -> ModelResponse:
        # model = await self.neural_network_repository.get_by_id(model)

        # if model is None:
        #     raise HTTPException(status_code=404, detail="Model not found")

        # user_requests = await self.user_requests_repository.get_by_user_and_model_id(
        #     model_id=model_id, user_id=request.user_id
        # )
        # amount = user_requests.amount
        # if amount == 0:
        #     return ModelResponse(value="Limit of free requests exceeded")

        response = await self.model_manager.generate_response(
            model_name=request.model, user_id=request.user_id, message=request.message
        )

        # await self.user_requests_repository.update(model_id=model_id, amount=0)

        return ModelResponse(value=response)
