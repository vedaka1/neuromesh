import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, cast

from httpx import AsyncClient

from domain.neural_networks.model import BaseTextModel
from infrastructure.config import settings

logger = logging.getLogger()


@dataclass
class Gigachat(BaseTextModel):

    url: str = field(
        default="https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
        init=False,
    )
    _access_token: str = field(default="", init=False)
    client: AsyncClient = field(
        default=AsyncClient(base_url="https://api-key.fusionbrain.ai/", verify=False),
        init=False,
    )
    auth_time: datetime | None = field(default=None, init=False)

    async def generate_response(
        self, user_id: uuid.UUID, message: dict[str, Any]
    ) -> str | None:
        await self._authenticate()

        try:
            payload = json.dumps(
                {
                    "model": "GigaChat",
                    "messages": [message],
                    "temperature": 1,
                    "stream": False,
                }
            )

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self._access_token}",
            }

            response = await self.client.post(
                url=self.url, headers=headers, data=payload  # type: ignore
            )

            response.raise_for_status()

            message = response.json()["choices"][0]["message"]["content"]

            return cast(str, message)

        except Exception as e:
            logger.error("User: %s, info: %s", user_id, e)

            return None

    async def _authenticate(self) -> None:
        if self.auth_time == None or datetime.now() >= self.auth_time + timedelta(
            minutes=25
        ):
            logger.info("Authenticating GigaChat")

            try:
                url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

                payload = "scope=GIGACHAT_API_PERS"

                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                    "RqUID": f"{uuid.uuid4()}",
                    "Authorization": f"Basic {settings.sber.AUTH_DATA_SBER}",
                }

                response = await self.client.post(
                    url=url, headers=headers, data=payload  # type: ignore
                )

                self.auth_time = datetime.now(timezone.utc)

                self._access_token = response.json()["access_token"]

                return None

            except Exception as e:
                logger.error("GigaChat Auth Error %s", e)

                raise Exception("GigaChat Auth Error")

    @staticmethod
    def create_message(message: str) -> dict[str, str]:
        """Adds the user's message to the message list"""
        return {"role": "user", "content": message}

    @classmethod
    def _test_access(cls) -> bool:
        return True
