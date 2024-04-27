from dataclasses import dataclass, field

from domain.common.response import Response
from domain.neural_networks.manager import BaseModelManager
from domain.neural_networks.model import BaseTextModel
from infrastructure.neural_networks.text_models import FreeChatGPT


class ModelManager(BaseModelManager):
    def __init__(self) -> None:
        self.models = {"chatgpt": FreeChatGPT()}

    async def generate_response(self, user_id, model_name, message) -> str:
        model: BaseTextModel = self.models.get(model_name, None)

        if model is None:
            raise ValueError(f"Model {model_name} not found")

        result = await model.generate_response(user_id, message)
        response = Response(result)

        return response.value
