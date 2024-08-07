from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from domain.common.response import Response
from infrastructure.config import settings
from presentation.common.texts import text


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: User = data["event_from_user"]
        if user.id == settings.HEAD_ADMIN_TG_ID:
            return await handler(event, data)
        return await event.answer(Response(text.permission_denied).value)
