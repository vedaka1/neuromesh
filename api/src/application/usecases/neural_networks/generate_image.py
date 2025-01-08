import logging
from dataclasses import dataclass

from application.common.tg_client import AsyncTGClient
from domain.neural_networks.model import BaseImageModel


@dataclass
class GenerateImage:
    tg_client: AsyncTGClient
    image_model: BaseImageModel

    async def __call__(self, user_id: int, user_prompt: str) -> None:
        logging.info('Generate image for user %i', user_id)

        response = await self.tg_client.post(
            'sendMessage',
            params={
                'chat_id': user_id,
                'text': '_Waiting_',
                'parse_mode': 'MarkDownV2',
            },
        )
        message = response.json()['result']

        try:
            image = await self.image_model.generate_response(user_prompt)
            if image:
                response = await self.tg_client.post(
                    'sendPhoto',
                    params={'chat_id': user_id},
                    files={'photo': image['image_base64']},
                )
                await self.tg_client.post(
                    'deleteMessage',
                    params={
                        'chat_id': user_id,
                        'message_id': message['message_id'],
                    },
                )
            else:
                await self.tg_client.post(
                    'editMessageText',
                    params={
                        'chat_id': user_id,
                        'message_id': message['message_id'],
                        'text': 'Время ожидания истекло',
                    },
                )

        except Exception as exc:
            logging.error(
                'Image generation for user %i failed',
                user_id,
                exc_info=exc,
                extra={'error': exc},
            )
            await self.tg_client.post(
                'editMessageText',
                params={
                    'chat_id': user_id,
                    'message_id': message['message_id'],
                    'text': 'Возникла ошибка',
                },
            )
            return None

        return None
