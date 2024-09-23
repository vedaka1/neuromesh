import logging
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

import google.generativeai as genai
from google.api_core.exceptions import FailedPrecondition

from domain.neural_networks.model import BaseTextModel
from infrastructure.config import settings

logger = logging.getLogger()


def init_gemini() -> genai.GenerativeModel:
    gemini = genai
    gemini.configure(api_key=settings.API_KEY_GEMINI)
    model = gemini.GenerativeModel("gemini-1.5-flash")
    return model


@dataclass
class Gemini(BaseTextModel):

    model: genai.GenerativeModel = field(default=init_gemini(), init=False)

    async def generate_response(
        self, user_id: UUID, message: dict[str, Any]
    ) -> str | None:
        try:
            result = await self.model.generate_content_async(message["parts"])
            return result.text
        except Exception as e:
            logger.error("User: %s, info: %s", user_id, e)
            raise

    @staticmethod
    def create_message(message: str) -> dict[str, Any]:
        return {"role": "user", "parts": [message]}

    @classmethod
    def _test_access(cls) -> bool:
        try:
            cls.model.generate_content("Hello")
            return True
        except FailedPrecondition:
            logger.error("Gemini not available. Setting status to False")
            return False
