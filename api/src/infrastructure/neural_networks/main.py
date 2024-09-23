import uuid
from dataclasses import dataclass, field
from enum import Enum

from fastapi import HTTPException

from domain.common.response import Response
from domain.exceptions.model import GenerationException, ModelUnavailableException
from domain.neural_networks.manager import BaseModelManager
from domain.neural_networks.model import BaseTextModel
from infrastructure.neural_networks.text_models import ChatGPT, FreeChatGPT, Gigachat


class NeuroModels(Enum):
    FREECHATGPT = "FreeChatGPT"
    GIGACHAT = "Gigachat"
    CHATGPT = "ChatGPT"
    GEMINI = "Gemini"


class ModelManager(BaseModelManager):
    def __init__(self) -> None:
        self.models = {
            NeuroModels.FREECHATGPT.value: FreeChatGPT(),
            NeuroModels.GIGACHAT.value: Gigachat(),
            NeuroModels.CHATGPT.value: ChatGPT(),
        }

    async def generate_response(
        self, user_id: uuid.UUID, model_name: str, message: str
    ) -> str:
        model: BaseTextModel | None = self.models.get(model_name, None)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        model_message = model.create_message(message=message)
        result = await model.generate_response(user_id, model_message)
        if result is None:
            raise ModelUnavailableException
        response = Response(result)
        return response.value
