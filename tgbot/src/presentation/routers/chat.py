from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from httpx import AsyncClient, HTTPStatusError

from domain.common.response import Response

chat_router = Router()


class Generate(StatesGroup):
    text = State()


@chat_router.message(Generate.text)
async def generate_error(message: types.Message) -> None:
    await message.reply("Подождите, ваше сообщение уже генерируется...")


@chat_router.message(filters.Command("imagine"))
async def generate_image(
    message: types.Message,
    state: FSMContext,
    client: AsyncClient,
    command: filters.command.CommandObject,
) -> None:
    await state.set_state(Generate.text)
    user_id = message.from_user.id
    prompt = command.args
    data = await client.post(
        "/models/image",
        params={
            "user_id": user_id,
            "user_prompt": prompt,
        },
        timeout=10,
    )
    data.raise_for_status()


@chat_router.message(F.text)
async def generate_response(
    message: types.Message, users: dict, state: FSMContext, client: AsyncClient
) -> None:
    await state.set_state(Generate.text)
    user_id = message.from_user.id
    if user_id not in users:
        await state.clear()
        return

    msg = await message.answer(text="_Waiting_ \U0001F551")
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
    await msg.edit_text(data.json()["value"])
    await state.clear()
