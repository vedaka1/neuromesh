from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from infrastructure.config import config
from presentation.common.texts import text
from src.application.common.response import Response


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: User = data['event_from_user']
        if user.id == config.telegram.HEAD_ADMIN_TG_ID:
            return await handler(event, data)
        return await event.answer(Response(text.permission_denied).value)
