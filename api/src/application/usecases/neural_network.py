from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.contracts.neural_networks.create_neural_network_request import (
    CreateNeuralNetworkRequest,
)
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
