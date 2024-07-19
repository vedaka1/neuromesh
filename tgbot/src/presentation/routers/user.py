from aiogram import Bot, F, Router, filters, types
from httpx import AsyncClient, HTTPStatusError

from domain.common.response import Response
from presentation.common.keyboards import kb

user_router = Router()


@user_router.message(filters.Command("start"))
async def cmd_start(message: types.Message, client: AsyncClient):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        response = await client.post(
            "/users",
            json={"telegram_id": user_id, "username": username},
        )
        response.raise_for_status()
        await message.answer(
            "Привет!\n" + "Доступные команды:\n" + " /select_model выбирает модель"
        )
    except HTTPStatusError as e:
        await message.answer(Response(f"Error: {e.response.json()["detail"]}").value)
    except Exception as e:
        await message.answer(f"Unknown error")


@user_router.message(filters.Command("account"))
async def cmd_start(message: types.Message, client: AsyncClient):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        response = await client.get(
            f"/users/{user_id}",
        )
        response.raise_for_status()
        user_data = response.json()
        text = (
            "Подписка: *"
            + user_data['subscription']['subscription_name']
            + "*\nКоличество запросов:\n"
        )
        for request in user_data['requests']:
            text += request['neural_network_name'] + ": *" + str(request['amount']) + "*\n" 
        await message.answer(text=text)
    except HTTPStatusError as e:
        await message.answer(Response(f"Error: {e.response.json()["detail"]}").value)
    except Exception as e:
        await message.answer(f"Unknown error")


@user_router.message(filters.Command("select_model"))
async def cmd_select_model(message: types.Message, client: AsyncClient):
    user_id = message.from_user.id
    user = await client.get(
        f"/users/{user_id}",
    )
    user = user.json()
    try:
        response = await client.get(
            f"/subscriptions/{user["subscription"]["subscription_name"]}",
        )
        response.raise_for_status()
        await message.answer(
            text="Выберите модель:",
            reply_markup=kb.select_model(user_id, response.json()),
        )
    except HTTPStatusError as e:
        await message.answer(Response(f"Error: {e.response.json()["detail"]}").value)
    except Exception as e:
        await message.answer(f"Unknown error")
    
    


@user_router.callback_query(F.data.startswith("selectModel_"))
async def callback_select_model(callback: types.CallbackQuery, users: dict, client: AsyncClient):
    data = callback.data.split("_")
    user_id, choice = int(data[1]), data[2]
    try:
        response = await client.get(
            f"/users/{user_id}",
        )
        response.raise_for_status()
        data = response.json()
        users[user_id] = {"id": data["id"], "model": choice}
        await callback.message.edit_text(text=f"Текущая модель: {choice}")
    except HTTPStatusError as e:
        await callback.message.answer(Response(f"Error: {e.response.json()["detail"]}").value)
    except Exception as e:
        await callback.message.answer(f"Unknown error")
    
