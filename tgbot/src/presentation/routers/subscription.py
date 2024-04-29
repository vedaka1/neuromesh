from aiogram import Bot, F, Router, filters, types
from httpx import AsyncClient

subscription_router = Router()


@subscription_router.message(filters.Command("subscriptions"))
async def get_all_subscriptions(message: types.Message, client: AsyncClient):
    data = await client.get("/subscriptions").json()
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
