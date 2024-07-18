import asyncio
import base64
import json

import httpx
from httpx import AsyncClient, Client, Response

from domain.neural_networks.model import BaseImageModel
from infrastructure.config import settings


class Kadinsky(BaseImageModel):
    def __init__(self):
        self.__AUTH_HEADERS = {
            "X-Key": f"Key {settings.API_KEY_KADINSKY}",
            "X-Secret": f"Secret {settings.API_SECRET_KEY_KADINSKY}",
        }
        self.client: AsyncClient = httpx.AsyncClient(
            base_url="https://api-key.fusionbrain.ai/key/api/v1",
            headers=self.__AUTH_HEADERS,
        )
        self.model_id = self.__get_model()

    def __get_model(self) -> int:
        with Client() as client:
            response: Response = client.get(
                "models",
                headers=self.__AUTH_HEADERS,
            )
            data = response.json()
            return data[0]["id"]

    async def generate_response(self, prompt: str) -> dict[bytes, str]:
        try:
            image_id = await self.generate_image(prompt=prompt)
            image = await self.check_generation(request_id=image_id)
            return {"image_base64": image, "image_id": image_id}
        except:
            raise Exception("Failed to generate image")

    async def generate_image(
        self, prompt: str, images=1, width=1024, height=1024
    ) -> str:
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {"query": f"{prompt}"},
        }
        data = {
            "params": (None, json.dumps(params), "application/json"),
        }
        response: Response = await self.client.post(
            "/text2image/run", params={"model_id": self.model_id}, files=data
        )
        data = response.json()
        return data["uuid"]

    async def check_generation(self, request_id: int, attempts=10, delay=10) -> bytes:
        while attempts > 0:
            response = await self.client.get(
                "/text2image/status/" + request_id,
                headers=self.__AUTH_HEADERS,
            )
            data = response.json()
            if data["status"] == "DONE":
                image = base64.b64decode(data["images"][0])
                return image

            attempts -= 1
            await asyncio.sleep(delay)
        return None
