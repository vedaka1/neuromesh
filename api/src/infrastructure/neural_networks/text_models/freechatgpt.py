import asyncio
import logging
import uuid
from dataclasses import dataclass
from typing import Any

import g4f
import g4f.Provider
from domain.neural_networks.model import BaseTextModel

g4f.debug.logging = False
_providers = [
    {'provider': g4f.Provider.GeminiPro, 'available': True},
    {'provider': g4f.Provider.Koala, 'available': True},
    {'provider': g4f.Provider.DDG, 'available': True},
    {'provider': g4f.Provider.Bing, 'available': True},
    {'provider': g4f.Provider.You, 'available': True},
    {'provider': g4f.Provider.FreeGpt, 'available': True},
    {'provider': g4f.Provider.GPTalk, 'available': True},
    {'provider': g4f.Provider.Hashnode, 'available': True},
    {'provider': g4f.Provider.FreeGpt, 'available': True},
    {'provider': g4f.Provider.Liaobots, 'available': True},
    {'provider': g4f.Provider.Chatgpt4Online, 'available': True},
    {'provider': g4f.Provider.FlowGpt, 'available': True},
    {'provider': g4f.Provider.GptTalkRu, 'available': True},
    {'provider': g4f.Provider.Vercel, 'available': True},
]


@dataclass
class FreeChatGPT(BaseTextModel):
    """FreeChatGPT class for bot users"""

    async def _run_provider(self, provider: g4f.Provider.BaseProvider, message: dict[str, Any], logs=False):
        """Runs the chat provider"""
        try:
            response = await g4f.ChatCompletion.create_async(  # type: ignore
                model=g4f.models.default,
                messages=[message],
                provider=provider,  # type: ignore
            )
            return response

        except Exception as e:
            if logs:
                logging.error('Provider: %s, info: %s', provider.__name__, e)

    async def generate_response(self, user_id: uuid.UUID, message: dict[str, Any]) -> str | None:
        """Generates responses from different providers"""
        calls = [self._run_provider(provider['provider'], message) for provider in _providers if provider['available']]
        responses = await asyncio.gather(*calls)
        for key, value in enumerate(responses):
            if value is None:
                _providers[key]['available'] = False

        result = [response for response in responses if response is not None and response != '']
        if result:
            logging.info('User: %s, chat_response: "%s"', user_id, result)
            return result[0]

        logging.error('User: %s, info: %s', user_id, responses)

    @staticmethod
    def create_message(message: str) -> dict[str, Any]:
        """Adds the user's message to the message list"""
        return {'role': 'user', 'content': message}

    @classmethod
    def _test_access(cls):
        return True
