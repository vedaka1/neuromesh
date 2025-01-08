from aiogram import F, Router, filters, types
from aiogram.fsm.context import FSMContext
from httpx import AsyncClient
from presentation.common.keyboards import kb
from presentation.common.states import (
    AddModelToSubscription,
    CreateModel,
    CreateSubscription,
)
from presentation.common.texts import text
from presentation.middlewares.admin import AdminMiddleware
from presentation.routers.subscription import get_all_subscriptions

from src.application.common.response import Response

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(filters.Command('info'))
async def cmd_info(message: types.Message):
    await message.answer(Response(text.info).value)


@admin_router.message(filters.Command('create_model'))
async def cmd_create_model(
    message: types.Message,
    state: FSMContext,
):
    await state.set_state(CreateModel.name)
    await message.answer('Write the name of model')


@admin_router.message(CreateModel.name)
async def cmd_create_model_name(
    message: types.Message,
    client: AsyncClient,
    state: FSMContext,
):
    response = await client.post('/models', params={'name': message.text})
    response.raise_for_status()
    await message.answer(text='Model created')
    await state.clear()


@admin_router.message(filters.Command('create_sub'))
async def cmd_create_sub(
    message: types.Message,
    state: FSMContext,
):
    await state.set_state(CreateSubscription.name)
    await message.answer('Write the name of subscription')


@admin_router.message(CreateSubscription.name)
async def cmd_create_sub_name(
    message: types.Message,
    client: AsyncClient,
    state: FSMContext,
):
    response = await client.post('/subscriptions', json={'name': message.text})
    response.raise_for_status()
    await state.clear()
    await message.answer('Subscription created')


@admin_router.message(filters.Command('models'))
async def cmd_models(
    message: types.Message,
    client: AsyncClient,
):
    response = await client.get('/models')
    response.raise_for_status()
    text = 'Available models:\n'
    for model in response.json():
        text += f"{model["name"]}\n"
    await message.answer(text=Response(text).value)


@admin_router.message(filters.Command('add_model_to_sub'))
async def cmd_add_model_to_sub_start(
    message: types.Message,
    client: AsyncClient,
    state: FSMContext,
):
    await state.set_state(AddModelToSubscription.subscription_name)
    await get_all_subscriptions(message, client)


@admin_router.callback_query(AddModelToSubscription.subscription_name, F.data.startswith('selectSub_'))
async def callback_add_model_to_sub(
    callback: types.CallbackQuery,
    client: AsyncClient,
    state: FSMContext,
):
    subscription_name = callback.data.split('_')[1]
    await state.update_data(subscription_name=subscription_name)
    await state.set_state(AddModelToSubscription.model_name)
    subscription_models = await client.get(f'/subscriptions/{subscription_name}')
    response = await client.get('/models')
    response.raise_for_status()
    sub_models = {item['name'] for item in subscription_models.json()['models']}
    all_models = {item['name'] for item in response.json()}
    models = all_models - sub_models
    if not models:
        await callback.message.edit_text('All available models already added to this subscription', reply_markup=None)
        await state.clear()
        return
    await callback.message.edit_text(text='Select model:', reply_markup=kb.all_models(models))


@admin_router.callback_query(AddModelToSubscription.model_name, F.data.startswith('selectModel_'))
async def callback_select_model(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    model = callback.data.split('_')[1]
    await state.update_data(model_name=model)
    await state.set_state(AddModelToSubscription.default_requests)
    await callback.message.edit_text('Write an amount of available requests to the model per week', reply_markup=None)


@admin_router.message(AddModelToSubscription.default_requests)
async def cmd_add_model_to_sub(
    message: types.Message,
    client: AsyncClient,
    state: FSMContext,
):
    await state.update_data(default_requests=message.text)
    data = await state.get_data()
    subscription_name = data.get('subscription_name', '')
    model_name = data.get('model_name', '')
    default_requests = data.get('default_requests', '')
    response = await client.post(
        f'/subscriptions/{subscription_name}',
        params={'model_name': model_name, 'default_requests': default_requests},
    )
    response.raise_for_status()
    await state.clear()
    await message.answer('Model added to subscription')


@admin_router.message(filters.Command('cancel'))
@admin_router.message(F.text.casefold() == 'cancel')
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(
        'Canceled',
    )


@admin_router.message(filters.Command('users'))
async def cmd_users(message: types.Message, client: AsyncClient):
    response = await client.get('/users')
    response.raise_for_status()
    text = 'Users:\n'
    for user in response.json():
        text += f"{user['username']}\n"
    await message.answer(text=Response(text).value)
