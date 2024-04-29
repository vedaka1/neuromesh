from aiogram import Bot, F, Router, filters, types
from httpx import AsyncClient, HTTPStatusError, TimeoutException

chat_router = Router()


@chat_router.message(filters.Command("startsss"))
async def cmd_start(message: types.Message, bot: Bot, client: AsyncClient):
    user_id = message.from_user.id
    data = await client.get("/subscriptions")
    print(data.json())
    username = message.from_user.username
    await bot.send_message(
        chat_id=426826549, text=f"New user _{username}_\\!", parse_mode="MarkDownV2"
    )
    await message.answer(
        "Привет!\n" + "Доступные команды:\n" + " /select_model выбирает модель"
    )


@chat_router.message(F.text)
async def echo(message: types.Message, users: dict, client: AsyncClient):
    user_id = message.from_user.id
    if user_id not in users:
        return
    msg = await message.answer(text="<i>Waiting</i> \U0001F551")
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
    except (HTTPStatusError, TimeoutException) as e:
        print(f"HTTP {e.response.status_code} Exception {e.response.text}")
        await message.answer("Не удалось получить ответ")
        return
    await msg.edit_text(data.json()["value"])
