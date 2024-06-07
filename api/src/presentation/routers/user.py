import uuid

from fastapi import APIRouter, Depends
from punq import Container

from application.contracts.users.get_user_response import GetUserResponse
from application.contracts.users.register_request import RegisterRequest
from application.usecases.user import UserService
from application.usecases.users import *
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
    create_user_interactor: CreateUser = container.resolve(CreateUser)
    return await create_user_interactor(create_user_request)


@user_router.delete("/{user_id}", description="Удаляет пользователя по id")
async def delete_user(
    user_id: int,
    container: Container = Depends(get_container),
):
    delete_user_interactor: DeleteUser = container.resolve(DeleteUser)
    return await delete_user_interactor(user_id)


@user_router.get("", description="Возвращает список пользователей")
async def get_users(
    container: Container = Depends(get_container),
):
    get_users_interactor: GetAllUsers = container.resolve(GetAllUsers)
    return await get_users_interactor()


@user_router.get(
    "/{user_id}",
    description="Получает пользователя по telegram_id",
    response_model=GetUserResponse,
)
async def get_user(
    user_id: int,
    container: Container = Depends(get_container),
):
    get_user_interactor: GetUserByTelegramId = container.resolve(GetUserByTelegramId)
    return await get_user_interactor(user_id)


@user_router.get("/{user_id}/requests", description="Получить лимиты пользователя")
async def get_user_requests(
    user_id: uuid.UUID,
    container: Container = Depends(get_container),
):
    get_user_requests_interactor: GetUserRequests = container.resolve(GetUserRequests)
    return await get_user_requests_interactor(user_id)


@user_router.put("/{user_id}/requests", description="Обновить лимиты пользователя")
async def update_user_requests(
    user_id: uuid.UUID, amount: int, container: Container = Depends(get_container)
):
    update_user_requests_interactor: UpdateUserRequests = container.resolve(
        UpdateUserRequests
    )
    return await update_user_requests_interactor(user_id, amount)


@user_router.get("/{user_id}/subscription", description="Получить все подписки")
async def get_user_subscriptions(
    user_id: uuid.UUID,
    container: Container = Depends(get_container),
):
    get_user_subscriptions_interactor: GetUserSubscriptions = container.resolve(
        GetUserSubscriptions
    )
    return await get_user_subscriptions_interactor(user_id)


@user_router.put("/{user_id}/subscription", description="Сменить подписку")
async def update_user_subscription(
    user_id: uuid.UUID,
    subscription_name: str,
    container: Container = Depends(get_container),
):
    change_user_subscription_interactor: ChangeUserSubscription = container.resolve(
        ChangeUserSubscription
    )
    return await change_user_subscription_interactor(user_id, subscription_name)
