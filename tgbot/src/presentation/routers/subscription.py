from aiogram import Bot, F, Router, filters, types
from httpx import AsyncClient, HTTPStatusError

from domain.common.response import Response
from presentation.common.keyboards import kb
from presentation.dependencies.user import get_user

subscription_router = Router()


@subscription_router.message(filters.Command("subscriptions"))
async def get_all_subscriptions(message: types.Message, client: AsyncClient):
    try:
        response = await client.get("/subscriptions")
        response.raise_for_status()
        await message.answer(
            text="Выберите подписку:",
            reply_markup=kb.all_subscriptions(response.json())
        )
    except HTTPStatusError as e:
        print(e)
        await message.answer(Response(f"Error: {e.response.json()["detail"]}").value)
    except Exception as e:
        print(e)
        await message.answer(f"Неизвестная ошибка")


@subscription_router.callback_query(F.data.startswith("selectSub_"))
async def select_subscription_callback(callback: types.CallbackQuery, client: AsyncClient):
    user_choice = callback.data.split("_")[1]
    user_id = callback.from_user.id
    user = await get_user(user_id, client)
    try:
        result = await client.put(f"/users/{user["id"]}/subscription", params={"subscription_name": user_choice})
        result.raise_for_status()
        await callback.message.edit_text("Выбрана подписка: " + user_choice)
    except HTTPStatusError as e:
        await callback.message.answer(Response(f"Error: {e.response.json()["detail"]}").value)
    except Exception as e:
        await callback.message.answer(f"Unknown error")     

