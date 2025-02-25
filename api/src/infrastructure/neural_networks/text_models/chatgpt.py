import logging
import uuid
from typing import Any

import openai
from domain.neural_networks.model import BaseTextModel
from openai.types.chat.chat_completion import ChatCompletion


class ChatGPT(BaseTextModel):
    """FreeChatGPT class for bot users"""

    def __init__(self, client: openai.AsyncOpenAI) -> None:
        self.client = client

    async def generate_response(
        self, user_id: uuid.UUID, message: dict[str, Any], *, model: str = 'gpt-4o-mini'
    ) -> str | None:
        """Generates responses from different providers"""
        try:
            result: ChatCompletion = await self.client.chat.completions.create(  # type: ignore
                model=model,
                messages=[message],  # type: ignore
                stream=False,
            )

            response = result.choices[0].message.content

            logging.info('User: %s, chat_response: "%s"', user_id, response)

            return response

        except openai.RateLimitError:
            if model == 'gpt-4o-mini':
                return await self.generate_response(user_id=user_id, message=message, model='gpt-3.5-turbo')
        except Exception as e:
            logging.error('User: %s, info: %s', user_id, e)

    @staticmethod
    def create_message(message: str) -> dict[str, Any]:
        """Adds the user's message to the message list"""
        return {'role': 'user', 'content': message}

    @classmethod
    def _test_access(cls):
        return True
