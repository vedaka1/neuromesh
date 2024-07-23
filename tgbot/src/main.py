import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from infrastructure.config import settings
from infrastructure.di.container import init_client, init_logger, init_loki_logger
from presentation.exc_handlers import init_exc_handlers
from presentation.routers.admin import admin_router
from presentation.routers.chat import chat_router
from presentation.routers.subscription import subscription_router
from presentation.routers.user import user_router


def init_routers(dp: Dispatcher):
    dp.include_router(admin_router)
    dp.include_router(subscription_router)
    dp.include_router(user_router)
    dp.include_router(chat_router)


async def main():
    init_logger()
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )
    dp = Dispatcher()
    init_routers(dp)
    dp["client"] = init_client()
    dp["users"] = {}
    await init_exc_handlers(dp)
    handler = init_loki_logger(app_name="tgbot")
    logging.getLogger("aiogram.event").addHandler(handler)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
