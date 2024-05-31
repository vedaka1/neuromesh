import uuid

from application.contracts.users.get_user_response import GetUserResponse
from application.contracts.users.register_request import RegisterRequest
from application.usecases.user import UserService
from domain.users.user import UserDB
from fastapi import APIRouter, Depends
from infrastructure.di.container import get_container
from punq import Container

user_router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@user_router.post("", description="Создает нового пользователя", response_model=UserDB)
async def create_user(
    create_user_request: RegisterRequest,
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.create(create_user_request)


@user_router.delete("/{user_id}", description="Удаляет пользователя по id")
async def delete_user(
    user_id: int,
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.delete_by_id(user_id)


@user_router.get("", description="Возвращает список пользователей")
async def get_users(
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.get_all()


@user_router.get(
    "/{user_id}",
    description="Получает пользователя по telegram_id",
    response_model=GetUserResponse,
)
async def get_user(
    user_id: int,
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.get_user_by_telegram_id(user_id)


@user_router.get("/{user_id}/requests", description="Получить лимиты пользователя")
async def get_user_requests(
    user_id: uuid.UUID,
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.get_user_requests(user_id)


@user_router.put("/{user_id}/requests", description="Обновить лимиты пользователя")
async def update_user_requests(
    user_id: uuid.UUID, amount: int, container: Container = Depends(get_container)
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.update_user_requests(user_id, amount)


@user_router.get("/{user_id}/subscription", description="Получить все подписки")
async def get_user_subscriptions(
    user_id: uuid.UUID,
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.get_user_subscriptions(user_id)


@user_router.put("/{user_id}/subscription", description="Сменить подписку")
async def update_user_subscription(
    user_id: uuid.UUID,
    subscription_name: str,
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.change_subscription(user_id, subscription_name)
