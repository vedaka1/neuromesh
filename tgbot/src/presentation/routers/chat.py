from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from httpx import AsyncClient, HTTPStatusError

chat_router = Router()


class Generate(StatesGroup):
    text = State()


@chat_router.message(Generate.text)
async def generate_error(message: types.Message) -> None:
    await message.reply("Подождите, ваше сообщение уже генерируется...")


@chat_router.message(F.text)
async def generate_response(
    message: types.Message, users: dict, state: FSMContext, client: AsyncClient
) -> None:
    await state.set_state(Generate.text)
    user_id = message.from_user.id
    if user_id not in users:
        return
    msg = await message.answer(text="_Waiting_ \U0001F551", parse_mode="MarkDownV2")
    try:
        data = await client.post(
            "/models/response",
            json={
                "model": users[user_id]["model"],
                "user_id": users[user_id]["id"],
                "message": message.text,
            },
            timeout=10,
        )
        data.raise_for_status()

    except HTTPStatusError as e:
        if e.response.status_code == 403:
            await msg.edit_text("У вас нет доступа к данной модели")
    except Exception as e:
        await msg.edit_text("Не удалось получить ответ")
    finally:
        await state.clear()

    await msg.edit_text(data.json()["value"], parse_mode="MarkDownV2")
    await state.clear()
