from dataclasses import dataclass

from application.common.transaction import BaseTransactionManager
from application.contracts.neural_networks.generate_response_request import (
    GenerateResponseRequest,
)
from domain.common.response import ModelResponse
from domain.exceptions.model import *
from domain.messages.message import Message
from domain.neural_networks.manager import BaseModelManager
from domain.neural_networks.repository import BaseNeuralNetworkRepository
from domain.users.repository import BaseUserRequestRepository


@dataclass
class GenerateResponse:

    user_requests_repository: BaseUserRequestRepository
    neural_network_repository: BaseNeuralNetworkRepository
    model_manager: BaseModelManager
    transaction_manager: BaseTransactionManager

    async def __call__(self, request: GenerateResponseRequest) -> ModelResponse:
        model = await self.neural_network_repository.get_by_name(request.model)

        base_prompt = "<system>\nДлина твоего ответа не должна превышать 4000 символов\n</system>\n"

        message = Message(base_prompt + request.message)

        if model is None:
            raise ModelNotFoundException

        user_requests = await self.user_requests_repository.get_by_user_and_model_name(
            model_name=model.name, user_id=request.user_id
        )

        if user_requests is None:
            raise NoAccessToModelException

        if user_requests.amount == 0:
            return ModelResponse(value="Limit of free requests exceeded")

        response = await self.model_manager.generate_response(
            model_name=request.model, user_id=request.user_id, message=message.value
        )

        await self.user_requests_repository.update_user_requests(
            user_id=request.user_id,
            model_name=model.name,
            amount=user_requests.amount - 1,
        )

        await self.transaction_manager.commit()

        return ModelResponse(value=response)
