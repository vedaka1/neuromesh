import json
import logging
import uuid
from datetime import datetime
from typing import Any, cast

import aiohttp
from domain.neural_networks.model import BaseTextModel

from infrastructure.config import config


class Gigachat(BaseTextModel):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session
        self.url: str = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
        self._access_token: str | None = None
        self.token_expired_at: datetime | None = None

    async def generate_response(self, user_id: uuid.UUID, message: dict[str, Any]) -> str | None:
        try:
            await self._authenticate()

            payload = json.dumps({'model': 'GigaChat', 'messages': [message], 'stream': False, 'update_interval': 0})
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self._access_token}',
            }

            response = await self.session.request('POST', url=self.url, headers=headers, data=payload, verify_ssl=False)
            response.raise_for_status()
            data = await response.json()

            message = data['choices'][0]['message']['content']
            return cast(str, message)

        except Exception as e:
            logging.error('User: %s, info: %s', user_id, e)

    async def _authenticate(self) -> None:
        if not self.token_expired_at or datetime.now() > self.token_expired_at:
            logging.info('Authenticating GigaChat')

            try:
                url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
                payload = 'scope=GIGACHAT_API_PERS'
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json',
                    'RqUID': f'{uuid.uuid4()}',
                    'Authorization': f'Basic {config.sber.AUTH_DATA_SBER}',
                }

                response = await self.session.request('POST', url=url, headers=headers, data=payload, verify_ssl=False)
                response.raise_for_status()
                data = await response.json()

                self.token_expired_at = datetime.fromtimestamp(data['expires_at'] / 1000)
                self._access_token = data['access_token']

            except Exception as e:
                logging.error('GigaChat Auth Error %s', e)
                raise Exception('GigaChat Auth Error')

    @staticmethod
    def create_message(message: str) -> dict[str, str]:
        """Adds the user's message to the message list"""
        return {'role': 'user', 'content': message}

    @classmethod
    def _test_access(cls) -> bool:
        return True
