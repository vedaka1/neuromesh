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
    # g4f.Provider.Aura,
    g4f.Provider.GeminiProChat,
    g4f.Provider.Koala,
    # g4f.Provider.Aichat,
    # g4f.Provider.ChatBase,
    # g4f.Provider.Bing,
    # g4f.Provider.GptGo,
    g4f.Provider.You,
    # g4f.Provider.Yqcloud,
    # g4f.Provider.GPTalk,
    g4f.Provider.Hashnode,
    g4f.Provider.FreeGpt,
    g4f.Provider.ChatgptAi,
    g4f.Provider.Liaobots,
    g4f.Provider.Chatgpt4Online,
    g4f.Provider.ChatgptNext,
    g4f.Provider.ChatgptX,
    g4f.Provider.GptForLove,
    g4f.Provider.FlowGpt,
    g4f.Provider.GptTalkRu,
    g4f.Provider.Vercel,
    g4f.Provider.Aichatos,
    g4f.Provider.Cnote,
    g4f.Provider.DuckDuckGo,
    g4f.Provider.Feedough,
]


@dataclass
class FreeChatGPT(BaseTextModel):
    """FreeChatGPT class for bot users"""

    logger: logging.Logger = field(default=logging.getLogger(), init=False)

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

    async def generate_response(self, user_id: uuid.UUID, message: str) -> str:
        """Generates responses from different providers"""
        calls = [self._run_provider(provider, message) for provider in _providers]
        responses = await asyncio.gather(*calls)
        result = [
            response
            for response in responses
            if response is not None and response != ""
        ]
        if result:
            # user.messages.append({"role": "assistant", "content": result[0]})
            response = Response(result[0])
            self.logger.info('User: %s, chat_response: "%s"', user_id, response.value)
            return response.value
        self.logger.error("User: %s, info: %s", user_id, responses)
        return False

    @staticmethod
    def create_message(message) -> dict[str, str]:
        """Adds the user's message to the message list"""
        return {"role": "user", "content": message}

    @classmethod
    def _test_access(cls):
        return True
