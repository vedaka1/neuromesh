from dataclasses import dataclass

from application.common.tg_client import AsyncTGClient
from domain.neural_networks.model import BaseImageModel


@dataclass
class GenerateImage:
    tg_client: AsyncTGClient
    image_model: BaseImageModel

    async def __call__(self, user_id: int, user_prompt: str) -> str:

        result = await self.tg_client.post(
            "sendMessage",
            params={"chat_id": user_id, "text": "<i>Waiting</i>", "parse_mode": "HTML"},
        )
        message = result.json()["result"]
        try:
            image = await self.image_model.generate_response(user_prompt)
            if image:
                result = await self.tg_client.post(
                    "sendPhoto",
                    params={"chat_id": user_id},
                    files={"photo": image["image_base64"]},
                )
                await self.tg_client.post(
                    "deleteMessage",
                    params={
                        "chat_id": user_id,
                        "message_id": message["message_id"],
                    },
                )
            else:
                await self.tg_client.post(
                    "editMessageText",
                    params={
                        "chat_id": user_id,
                        "message_id": message["message_id"],
                        "text": "Время ожидания истекло",
                    },
                )

        except Exception as e:
            await self.tg_client.post(
                "editMessageText",
                params={
                    "chat_id": user_id,
                    "message_id": message["message_id"],
                    "text": "Возникла ошибка",
                },
            )
