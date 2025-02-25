from uuid import uuid4

from aiogram import F, Router, types
from infrastructure.gateways.twitter import TwitterGateway

videos_router = Router()


@videos_router.message(F.text)
async def download_video_from_url(message: types.Message) -> None:
    if not message.text:
        return
    elif not message.text.startswith('https://x.com'):
        return

    video_url = message.text
    if not video_url:
        await message.answer('Provide a valid url after the command')
        return

    downloader = TwitterGateway()
    buffer = await downloader.download_video(video_url)
    if not buffer:
        await message.answer('Could not download video')
        return

    video = types.BufferedInputFile(file=buffer, filename=str(uuid4()))
    await message.answer_video(video)
