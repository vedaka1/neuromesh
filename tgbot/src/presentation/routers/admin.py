from aiogram import Router, filters, types
from httpx import AsyncClient, HTTPStatusError

from domain.common.response import Response
from presentation.common.texts import text
from presentation.middlewares.admin import AdminMiddleware

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(filters.Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(Response(text.info).value)


@admin_router.message(filters.Command("create_model"))
async def cmd_create_model(
    message: types.Message,
    client: AsyncClient,
    command: filters.command.CommandObject,
):
    try:
        args = command.args.split()
        response = await client.post("/models", params={"name": args[0]})
        response.raise_for_status()
        await message.answer("Модель создана")
    except HTTPStatusError as e:
        await message.answer(Response(f"Error: {e.response.json()["detail"]}").value)
    except Exception as e:
        print(e)
        await message.answer(f"Неизвестная ошибка")


@admin_router.message(filters.Command("create_sub"))
async def cmd_create_sub(
    message: types.Message,
    client: AsyncClient,
    command: filters.command.CommandObject,
):
    try:
        args = command.args.split()
        response = await client.post("/subscriptions", json={"name": args[0]})
        response.raise_for_status()
        await message.answer("Подписка создана")
    except HTTPStatusError as e:
        await message.answer(Response(f"Error: {e.response.json()["detail"]}").value)
    except Exception as e:
        await message.answer(f"Unknown error")


@admin_router.message(filters.Command("models"))
async def cmd_modelss(
    message: types.Message,
    client: AsyncClient,
):
    try:
        response = await client.get("/models")
        response.raise_for_status()
        text = "Доступные модели:\n"
        for model in response.json():
            text += f"{model["name"]}\n"
        await message.answer(text=Response(text).value)
    except HTTPStatusError as e:
        await message.answer(Response(f"Ошибка: {e}").value)
    except Exception as e:
        print(e)
        await message.answer(f"Неизвестная ошибка")


@admin_router.message(filters.Command("add_model_to_sub"))
async def cmd_add_model_to_sub(
    message: types.Message,
    client: AsyncClient,
    command: filters.command.CommandObject,
):
    try:
        args = command.args.split()
        response = await client.post(
            f"/subscriptions/{args[0]}",
            params={"model_name": args[1], "default_requests": args[2]},
        )
        response.raise_for_status()
        await message.answer("Модель добавлена в подписку")
    except HTTPStatusError as e:
        await message.answer(Response(f"Ошибка: {e}").value)
    except Exception as e:
        await message.answer(f"Неизвестная ошибка")
