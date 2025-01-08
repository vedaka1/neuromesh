from aiogram import F, Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from application.common.response import Response
from httpx import AsyncClient

chat_router = Router()


class GenerateText(StatesGroup):
    text = State()


@chat_router.message(GenerateText.text)
async def generate_error(message: types.Message) -> None:
    await message.reply(Response('Wait, your message is being generated...').value)


@chat_router.message(filters.Command('imagine'))
async def generate_image(
    message: types.Message,
    client: AsyncClient,
    command: filters.command.CommandObject,
) -> None:
    user_id = message.from_user.id
    prompt = command.args
    response = await client.post(
        '/models/image',
        params={
            'user_id': user_id,
            'user_prompt': prompt,
        },
    )
    response.raise_for_status()


@chat_router.message(F.text)
async def generate_response(message: types.Message, users: dict, state: FSMContext, client: AsyncClient) -> None:
    user_id = message.from_user.id
    if user_id not in users:
        return
    await state.set_state(GenerateText.text)
    msg = await message.answer(text='_Waiting_ \U0001f551')
    response = await client.post(
        '/models/response',
        json={
            'model': users[user_id]['model'],
            'user_id': users[user_id]['id'],
            'message': message.text,
        },
    )
    response.raise_for_status()
    await msg.edit_text(response.json()['value'])
    await state.clear()
