from dataclasses import dataclass, field

from domain.common.response import Response
from domain.exeptions.model import GenerationException
from domain.neural_networks.manager import BaseModelManager
from domain.neural_networks.model import BaseTextModel
from fastapi import HTTPException
from infrastructure.neural_networks.text_models import ChatGPT, FreeChatGPT, Gigachat


class ModelManager(BaseModelManager):
    def __init__(self) -> None:
        self.models = {
            "FreeChatGPT": FreeChatGPT(),
            "Gigachat": Gigachat(),
            "ChatGPT": ChatGPT(),
        }

    async def generate_response(self, user_id, model_name, message) -> str:
        model: BaseTextModel = self.models.get(model_name, None)

        if model is None:
            raise ValueError(f"Model {model_name} not found")

        result = await model.generate_response(user_id, message)
        if result is None:
            raise HTTPException(
                status_code=503, detail=f"{model_name} currently unavailable"
            )
        response = Response(result)
        return response.value
