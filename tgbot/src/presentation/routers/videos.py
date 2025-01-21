from uuid import uuid4

from aiogram import Router, filters, types

from infrastructure.gateways.twitter import TwitterGateway

videos_router = Router()


@videos_router.message(filters.Command('load'))
async def download_video_from_url(message: types.Message, command: filters.command.CommandObject) -> None:
    video_url = command.args
    if not video_url:
        await message.answer('Provide a valid url after the command')
        return

    downloader = TwitterGateway()
    buffer = await downloader.download_video(video_url)
    if not buffer:
        await message.answer('Could not download video')
        return

    image = types.BufferedInputFile(file=buffer, filename=str(uuid4()))
    await message.answer_photo(image)
