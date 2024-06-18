import logging
import uuid
from dataclasses import dataclass, field

import openai
from domain.neural_networks.model import BaseTextModel
from infrastructure.config import settings
from openai.types.chat.chat_completion import ChatCompletion


@dataclass
class ChatGPT(BaseTextModel):
    """FreeChatGPT class for bot users"""

    logger: logging.Logger = field(default=logging.getLogger(), init=False)
    client: openai.AsyncOpenAI = field(
        default=openai.AsyncOpenAI(api_key=settings.API_KEY_CHATGPT), init=False
    )

    async def generate_response(
        self, user_id: uuid.UUID, message: str, *, model: str = "gpt-3.5-turbo"
    ) -> str | None:
        """Generates responses from different providers"""
        try:
            result: ChatCompletion = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                stream=False,
            )
            response = result.choices[0].message.content
            self.logger.info('User: %s, chat_response: "%s"', user_id, response)
            return response

        except Exception as e:
            self.logger.error("User: %s, info: %s", user_id, e)
            return None

    @staticmethod
    def create_message(message) -> dict[str, str]:
        """Adds the user's message to the message list"""
        return {"role": "user", "content": message}

    @classmethod
    def _test_access(cls):
        return True
