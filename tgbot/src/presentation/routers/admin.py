from aiogram import F, Router, filters, types
from aiogram.fsm.context import FSMContext
from httpx import AsyncClient

from domain.common.response import Response
from presentation.common.keyboards import kb
from presentation.common.states import (
    AddModelToSubscription,
    CreateModel,
    CreateSubscription,
)
from presentation.common.texts import text
from presentation.middlewares.admin import AdminMiddleware
from presentation.routers.subscription import get_all_subscriptions

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(filters.Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(Response(text.info).value)


@admin_router.message(filters.Command("create_model"))
async def cmd_create_model(
    message: types.Message,
    state: FSMContext,
):
    await state.set_state(CreateModel.name)
    await message.answer("Напишите название модели нейросети")

@admin_router.message(CreateModel.name)
async def cmd_create_model(
    message: types.Message,
    client: AsyncClient,
    state: FSMContext,
):
    response = await client.post("/models", params={"name": message.text})
    response.raise_for_status()
    await message.answer(text="Модель создана")
    await state.clear()


@admin_router.message(filters.Command("create_sub"))
async def cmd_create_sub(
    message: types.Message,
    state: FSMContext,
):
    await state.set_state(CreateSubscription.name)
    await message.answer("Напишите название подписки")


@admin_router.message(CreateSubscription.name)
async def cmd_create_sub(
    message: types.Message,
    client: AsyncClient,
    state: FSMContext,
):
    response = await client.post("/subscriptions", json={"name": message.text})
    response.raise_for_status()
    await state.clear()
    await message.answer("Подписка создана")


@admin_router.message(filters.Command("models"))
async def cmd_models(
    message: types.Message,
    client: AsyncClient,
):
    response = await client.get("/models")
    response.raise_for_status()
    text = "Доступные модели:\n"
    for model in response.json():
        text += f"{model["name"]}\n"
    await message.answer(text=Response(text).value)


@admin_router.message(filters.Command("add_model_to_sub"))
async def cmd_add_model_to_sub(
    message: types.Message,
    client: AsyncClient,
    state: FSMContext,
):
    await state.set_state(AddModelToSubscription.subscription_name)
    await get_all_subscriptions(message, client)

        
@admin_router.callback_query(AddModelToSubscription.subscription_name, F.data.startswith("selectSub_"))
async def callback_add_model_to_sub(
    callback: types.CallbackQuery,
    client: AsyncClient,
    state: FSMContext,
):
    subscription = callback.data.split("_")[1]
    await state.update_data(subscription_name=subscription)
    await state.set_state(AddModelToSubscription.model_name)
    response = await client.get("/models")
    response.raise_for_status()
    await callback.message.edit_text(
        text="Выберите модель:",
        reply_markup=kb.all_models(response.json())
    )


@admin_router.callback_query(AddModelToSubscription.model_name, F.data.startswith("selectModel_"))
async def callback_select_model(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    model = callback.data.split("_")[1]
    await state.update_data(model_name=model)
    await state.set_state(AddModelToSubscription.default_requests)
    await callback.message.edit_text("Напишите доступное количество запросов к модели в неделю" ,reply_markup=None)

@admin_router.message(AddModelToSubscription.default_requests)
async def cmd_add_model_to_sub(
    message: types.Message,
    client: AsyncClient,
    state: FSMContext,
):
    await state.update_data(default_requests=message.text)
    data = await state.get_data()
    subscription_name = data.get("subscription_name", "")
    model_name = data.get("model_name", "")
    default_requests = data.get("default_requests", "")
    response = await client.post(
        f"/subscriptions/{subscription_name}",
        params={"model_name": model_name, "default_requests": default_requests},
    )
    response.raise_for_status()
    await state.clear()
    await message.answer("Модель добавлена в подписку")
