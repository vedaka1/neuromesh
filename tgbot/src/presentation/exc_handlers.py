from aiogram import Dispatcher, F, types
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from httpx import HTTPStatusError

from application.common.response import Response


async def init_exc_handlers(dp: Dispatcher) -> None:
    @dp.error(ExceptionTypeFilter(HTTPStatusError), F.update.message.as_('message'))
    async def handle_httpx_exception_message(error_event: types.ErrorEvent, message: types.Message, state: FSMContext):
        await state.clear()
        if error_event.exception.response.status_code == 422:
            return message.answer(
                text=f"{error_event.exception.response.json().get("detail", "efw")[0].get("msg", "Unprocessable entity")}"
            )
        await message.answer(
            text=Response(f"Error: {error_event.exception.response.json().get("detail", "Неизвестная ошибка")}").value
        )

    @dp.error(ExceptionTypeFilter(HTTPStatusError), F.update.callback_query.as_('callback'))
    async def handle_httpx_exception_callback(
        error_event: types.ErrorEvent, callback: types.CallbackQuery, state: FSMContext
    ):
        await state.clear()
        if error_event.exception.response.status_code == 422:
            return callback.message.answer(
                text=f"{error_event.exception.response.json().get("detail", "efw")[0].get("msg", "Unprocessable entity")}"
            )
        await callback.message.answer(
            text=Response(f"Error: {error_event.exception.response.json().get("detail", "Неизвестная ошибка")}").value
        )
