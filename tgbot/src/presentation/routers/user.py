from aiogram import Bot, F, Router, filters, types
from httpx import AsyncClient, HTTPStatusError

user_router = Router()


@user_router.message(filters.Command("start"))
async def cmd_start(message: types.Message, client: AsyncClient):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        data = await client.post(
            "/users",
            json={"telegram_id": user_id, "username": username},
        )
        data.raise_for_status()
    except HTTPStatusError as e:
        print(f"HTTP {e.response.status_code} Exception {e.response.text}")
        await message.answer("Ошибка при создании пользователя")

    await message.answer(
        "Привет!\n" + "Доступные команды:\n" + " /select_model выбирает модель"
    )


@user_router.message(filters.Command("account"))
async def cmd_start(message: types.Message, client: AsyncClient):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        data = await client.get(
            f"/users/{user_id}",
        )
        data.raise_for_status()
    except HTTPStatusError as e:
        print(f"HTTP {e.response.status_code} Exception {e.response.text}")
        await message.answer("Не удалось получить ответ")
        return
    user_data = data.json()
    text = (
        "Подписка: <b>"
        + user_data['subscription']['subscription_name']
        + "</b>\nКоличество запросов:\n"
    )
    for request in user_data['requests']:
        text += request['neural_network_name'] + ": <b>" + str(request['amount']) + "</b>\n" 
    await message.answer(text=text)


@user_router.message(filters.Command("select_model"))
async def cmd_select_model(message: types.Message, client: AsyncClient):
    user_id = message.from_user.id
    user = await client.get(
        f"/users/{user_id}",
    )
    user = user.json()
    try:
        data = await client.get(
            f"/subscriptions/{user["subscription"]["subscription_name"]}",
        )
        data.raise_for_status()
    except HTTPStatusError as e:
        print(f"HTTP {e.response.status_code} Exception {e.response.text}")
        await message.answer("Ошибка при получении моделей")
    buttons = [
        [
            types.InlineKeyboardButton(
                text=model["name"], callback_data=f"selectModel_{user_id}_{model["name"]}"
            )
        ]
        for model in data.json()["models"]
    ]
    await message.answer(
        text="Выберите модель:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons),
    )


@user_router.callback_query(F.data.startswith("selectModel_"))
async def callback_select_model(callback: types.CallbackQuery, users: dict, client: AsyncClient):
    data = callback.data.split("_")
    user_id, choice = int(data[1]), data[2]
    try:
        data = await client.get(
            f"/users/{user_id}",
        )
        data.raise_for_status()
    except HTTPStatusError as e:
        print(f"HTTP {e.response.status_code} Exception {e.response.text}")
        await callback.message.answer("Не удалось получить данные")
        return
    data = data.json()
    users[user_id] = {"id": data["id"], "model": choice}
    await callback.message.edit_text(text=f"Текущая модель: {choice}")
