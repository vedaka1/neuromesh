from dataclasses import dataclass

from application.common.transaction import ICommiter
from application.contracts.neural_networks.generate_response_request import (
    GenerateResponseRequest,
)
from domain.common.response import ModelResponse
from domain.exceptions.model import ModelNotFoundException, NoAccessToModelException
from domain.messages.message import Message
from domain.neural_networks.manager import BaseModelManager
from domain.neural_networks.repository import BaseNeuralNetworkRepository
from domain.users.repository import BaseUserRequestRepository


@dataclass
class GenerateResponse:
    user_requests_repository: BaseUserRequestRepository
    neural_network_repository: BaseNeuralNetworkRepository
    model_manager: BaseModelManager
    commiter: ICommiter

    async def __call__(self, request: GenerateResponseRequest) -> ModelResponse:
        model = await self.neural_network_repository.get_by_name(request.model)
        if not model:
            raise ModelNotFoundException

        user_requests = await self.user_requests_repository.get_by_user_and_model_name(model.name, request.user_id)
        if not user_requests:
            raise NoAccessToModelException
        if user_requests.amount == 0:
            return ModelResponse(value='Limit of free requests exceeded')

        message = Message(request.message).value
        response = await self.model_manager.generate_response(request.user_id, request.model, message)

        await self.user_requests_repository.update_user_requests(request.user_id, model.name, user_requests.amount - 1)
        await self.commiter.commit()

        return ModelResponse(value=response)
