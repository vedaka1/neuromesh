import uuid

from fastapi import APIRouter, Depends
from punq import Container

from application.contracts.users.register_request import RegisterRequest
from application.usecases.user import UserService
from domain.users.user import UserDB
from infrastructure.di.container import get_container

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


@user_router.get(
    "/{user_id}",
    description="Получает пользователя по telegram_id",
    response_model=UserDB,
)
async def get_user(
    user_id: int,
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.get_user_by_telegram_id(user_id)


@user_router.delete("", description="Удаляет пользователя по id")
async def delete_user(
    user_id: int,
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.delete_by_id(user_id)


@user_router.get("/{user_id}/requests", description="Возвращает лимиты пользователя")
async def get_user_requests(
    user_id: uuid.UUID,
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.get_user_requests(user_id)


@user_router.get("", description="Возвращает список пользователей")
async def get_users(
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.get_all()
