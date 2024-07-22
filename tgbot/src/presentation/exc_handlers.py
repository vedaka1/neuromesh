
from aiogram import Dispatcher, F, types
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from httpx import HTTPStatusError

from domain.common.response import Response


async def init_exc_handlers(dp: Dispatcher) -> None:
    @dp.error(ExceptionTypeFilter(HTTPStatusError), F.update.message.as_("message"))
    async def handle_httpx_exception(event: types.ErrorEvent, message: types.Message, state: FSMContext):
        await state.clear()
        if event.exception.response.status_code == 422:
            return await message.answer(text=f"{event.exception.response.json().get("detail", "efw")[0].get("msg", "Unprocessable entity")}")
        await message.answer(
            text=Response(
                f"Error: {event.exception.response.json().get("detail", "Неизвестная ошибка")}"
                ).value
        )
