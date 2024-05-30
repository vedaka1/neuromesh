import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.config import settings
from infrastructure.di.container import init_client, init_logger
from presentation.routers.chat import chat_router
from presentation.routers.subscription import subscription_router
from presentation.routers.user import user_router


def init_routers(dp: Dispatcher):
    dp.include_router(subscription_router)
    dp.include_router(user_router)
    dp.include_router(chat_router)


async def main():
    init_logger()
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    init_routers(dp)
    dp["client"] = init_client()
    dp["users"] = {}
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
