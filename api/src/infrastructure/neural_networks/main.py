import uuid
from enum import Enum

from domain.common.response import Response
from domain.exceptions.model import ModelUnavailableException
from domain.neural_networks.manager import BaseModelManager
from domain.neural_networks.model import BaseTextModel

from infrastructure.neural_networks.text_models import ChatGPT, Gigachat


class NeuroModels(Enum):
    FREECHATGPT = 'FreeChatGPT'
    GIGACHAT = 'Gigachat'
    CHATGPT = 'ChatGPT'
    GEMINI = 'Gemini'


class ModelManager(BaseModelManager):
    def __init__(self, gigachat: Gigachat, chatgpt: ChatGPT) -> None:
        self.models = {
            NeuroModels.GIGACHAT.value: gigachat,
            NeuroModels.CHATGPT.value: chatgpt,
        }

    async def generate_response(self, user_id: uuid.UUID, model_name: str, message: str) -> str:
        model: BaseTextModel | None = self.models.get(model_name, None)
        if not model:
            raise ValueError(f'Model {model_name} not found')

        model_message = model.create_message(message=message)
        result = await model.generate_response(user_id, model_message)
        if not result:
            raise ModelUnavailableException

        return Response(result).value
