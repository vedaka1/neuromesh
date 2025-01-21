from aiogram import F, Router, filters, types
from httpx import AsyncClient
from presentation.common.keyboards import kb
from presentation.dependencies.user import get_user

subscription_router = Router()


@subscription_router.message(filters.Command('subscriptions'))
async def get_all_subscriptions(message: types.Message, client: AsyncClient):
    response = await client.get('/subscriptions')
    response.raise_for_status()
    await message.answer(text='Select subscription:', reply_markup=kb.all_subscriptions(response.json()))


@subscription_router.callback_query(F.data.startswith('selectSub_'))
async def select_subscription_callback(callback: types.CallbackQuery, client: AsyncClient):
    user_choice = callback.data.split('_')[1]
    user_id = callback.from_user.id
    user = await get_user(user_id, client)
    response = await client.put(f'/users/{user["id"]}/subscription', params={'subscription_name': user_choice})
    response.raise_for_status()
    await callback.message.edit_text('Selected subscription: ' + user_choice)
