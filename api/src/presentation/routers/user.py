import uuid

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from application.contracts.users.get_user_requests import GetUserRequestsResponse
from application.contracts.users.get_user_response import GetUserResponse
from application.contracts.users.get_user_subscriptions_response import (
    GetUserSubscriptionResponse,
)
from application.contracts.users.register_request import RegisterRequest
from application.usecases.users import *
from domain.users.user import UserDB

user_router = APIRouter(
    tags=["Users"],
    prefix="/users",
    route_class=DishkaRoute,
)


@user_router.post("", description="Создает нового пользователя", response_model=UserDB)
async def create_user(
    create_user_request: RegisterRequest, create_user_interactor: FromDishka[CreateUser]
):
    return await create_user_interactor(create_user_request)


@user_router.delete("/{user_id}", description="Удаляет пользователя по id")
async def delete_user(
    user_id: int,
    delete_user_interactor: FromDishka[DeleteUser],
):
    return await delete_user_interactor(user_id)


@user_router.get(
    "", description="Возвращает список пользователей", response_model=list[UserDB]
)
async def get_users(
    get_users_interactor: FromDishka[GetAllUsers],
):
    return await get_users_interactor()


@user_router.get(
    "/{user_id}",
    description="Получает пользователя по telegram_id",
    response_model=GetUserResponse,
)
async def get_user(user_id: int, get_user_interactor: FromDishka[GetUserByTelegramId]):
    return await get_user_interactor(user_id)


@user_router.get(
    "/{user_id}/requests",
    description="Получить лимиты пользователя",
    response_model=list[GetUserRequestsResponse],
)
async def get_user_requests(
    user_id: uuid.UUID, get_user_requests_interactor: FromDishka[GetUserRequests]
):
    return await get_user_requests_interactor(user_id)


@user_router.put("/{user_id}/requests", description="Обновить лимиты пользователя")
async def update_user_requests(
    user_id: uuid.UUID,
    model_name: str,
    amount: int,
    update_user_requests_interactor: FromDishka[UpdateUserRequests],
):
    return await update_user_requests_interactor(user_id, model_name, amount)


@user_router.get(
    "/{user_id}/subscription",
    description="Возвращает текущую подписку пользователя, если она есть",
    response_model=GetUserSubscriptionResponse | None,
)
async def get_user_subscription(
    user_id: uuid.UUID,
    get_user_subscriptions_interactor: FromDishka[GetUserSubscription],
):
    return await get_user_subscriptions_interactor(user_id)


@user_router.get(
    "/{user_id}/subscriptions",
    description="Возвращает все подписки пользователя",
    response_model=list[GetUserSubscriptionResponse],
)
async def get_user_subscriptions(
    user_id: uuid.UUID,
    get_user_subscriptions_interactor: FromDishka[GetUserSubscriptions],
):
    return await get_user_subscriptions_interactor(user_id)


@user_router.put("/{user_id}/subscription", description="Сменить подписку")
async def update_user_subscription(
    user_id: uuid.UUID,
    subscription_name: str,
    change_user_subscription_interactor: FromDishka[UpdateUserSubscription],
):
    return await change_user_subscription_interactor(user_id, subscription_name)
