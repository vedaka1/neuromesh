import asyncio
import logging
import uuid
from dataclasses import dataclass, field

import g4f
import g4f.Provider

from domain.common.response import Response
from domain.neural_networks.model import BaseTextModel
from domain.users.user import User
from infrastructure.config import settings

g4f.debug.logging = False
_providers = [
    # {"provider": g4f.Provider.GeminiProChat, "available": True},
    # {"provider": g4f.Provider.Koala, "available": True},
    # {"provider": g4f.Provider.Aichat, "available": True},
    # {"provider": g4f.Provider.ChatBase, "available": True},
    # {"provider": g4f.Provider.Bing, "available": True},
    # {"provider": g4f.Provider.GptGo, "available": True},
    # {"provider": g4f.Provider.You, "available": True},
    # {"provider": g4f.Provider.Yqcloud, "available": True},
    # {"provider": g4f.Provider.GPTalk, "available": True},
    # {"provider": g4f.Provider.Hashnode, "available": True},
    {"provider": g4f.Provider.FreeGpt, "available": True},
    {"provider": g4f.Provider.ChatgptAi, "available": True},
    {"provider": g4f.Provider.Liaobots, "available": True},
    {"provider": g4f.Provider.Chatgpt4Online, "available": True},
    {"provider": g4f.Provider.ChatgptNext, "available": True},
    {"provider": g4f.Provider.ChatgptX, "available": True},
    {"provider": g4f.Provider.GptForLove, "available": True},
    {"provider": g4f.Provider.FlowGpt, "available": True},
    {"provider": g4f.Provider.GptTalkRu, "available": True},
    {"provider": g4f.Provider.Vercel, "available": True},
    {"provider": g4f.Provider.Aichatos, "available": True},
    {"provider": g4f.Provider.Cnote, "available": True},
    {"provider": g4f.Provider.DuckDuckGo, "available": True},
    {"provider": g4f.Provider.Feedough, "available": True},
]


@dataclass
class FreeChatGPT(BaseTextModel):
    """FreeChatGPT class for bot users"""

    logger: logging.Logger = field(default=logging.getLogger(__name__), init=False)

    async def _run_provider(
        self, provider: g4f.Provider.BaseProvider, message: str, logs=False
    ):
        """Runs the chat provider"""
        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.default,
                messages=[{"role": "user", "content": message}],
                provider=provider,
            )
            return response

        except Exception as e:
            if logs:
                self.logger.error("Provider: %s, info: %s", provider.__name__, e)
            return None

    async def generate_response(self, user_id: uuid.UUID, message: str) -> str | None:
        """Generates responses from different providers"""
        calls = [
            self._run_provider(provider["provider"], message)
            for provider in _providers
            if provider["available"]
        ]
        responses = await asyncio.gather(*calls)
        for key, value in enumerate(responses):
            if value is None:
                _providers[key]["available"] = False

        result = [
            response
            for response in responses
            if response is not None and response != ""
        ]
        if result:
            # user.messages.append({"role": "assistant", "content": result[0]})
            response = result[0]
            self.logger.info('User: %s, chat_response: "%s"', user_id, response)
            return response
        self.logger.error("User: %s, info: %s", user_id, responses)
        return None

    @staticmethod
    def create_message(message: str) -> dict[str, str]:
        """Adds the user's message to the message list"""
        return {"role": "user", "content": message}

    @classmethod
    def _test_access(cls):
        return True
