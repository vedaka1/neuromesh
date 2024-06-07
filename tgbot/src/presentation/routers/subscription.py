from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from httpx import AsyncClient, HTTPStatusError

from presentation.dependencies.user import get_user

subscription_router = Router()


@subscription_router.message(filters.Command("subscriptions"))
async def get_all_subscriptions(message: types.Message, client: AsyncClient):
    data = await client.get("/subscriptions")
    buttons = [
        [
            types.InlineKeyboardButton(
                text=sub["name"], callback_data=f"selectSub_{sub["name"]}"
            )
        ]
        for sub in data.json()
    ]
    await message.answer(
        text="Выберите подписку:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons),
    )


@subscription_router.callback_query(F.data.startswith("selectSub_"))
async def select_subscription_callback(callback: types.CallbackQuery, client: AsyncClient):
    user_choice = callback.data.split("_")[1]
    user_id = callback.from_user.id
    user = await get_user(user_id, client)
    try:
        result = await client.put(f"/users/{user["id"]}/subscription", params={"subscription_name": user_choice})
        result.raise_for_status()
        await callback.message.edit_text("Выбрана подписка: " + user_choice)
    except HTTPStatusError:
        await callback.message.answer("Ошибка при выборе подписки")
                

