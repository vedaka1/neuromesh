import logging

from application.usecases.neural_networks.generate_image import GenerateImage
from infrastructure.di.container import get_container
from infrastructure.tasks.main import broker

logging.getLogger('httpx').setLevel(logging.WARNING)


@broker.task
async def generate_image_task(user_id: int, user_prompt: str) -> None:
    di_container = get_container()
    async with di_container() as container:
        generate_image_interactor = await container.get(GenerateImage)
        await generate_image_interactor(user_id, user_prompt)
