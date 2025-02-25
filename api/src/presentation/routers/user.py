import uuid

from application.contracts.users.get_user_requests import GetUserRequestsResponse
from application.contracts.users.get_user_response import GetUserResponse
from application.contracts.users.get_user_subscriptions_response import (
    GetUserSubscriptionResponse,
)
from application.contracts.users.register_request import RegisterRequest
from application.usecases.users import DeleteUser, GetAllUsers
from application.usecases.users.create_user import CreateUser
from application.usecases.users.get_user import (
    GetUserByTelegramId,
    GetUserRequests,
    GetUserSubscription,
    GetUserSubscriptions,
)
from application.usecases.users.update_user import UpdateUserRequests, UpdateUserSubscription
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from domain.users.user import UserDB
from fastapi import APIRouter

user_router = APIRouter(
    tags=['Users'],
    prefix='/users',
    route_class=DishkaRoute,
)


@user_router.post('', summary='Creates a new user', response_model=UserDB)
async def create_user(create_user_request: RegisterRequest, create_user_interactor: FromDishka[CreateUser]) -> UserDB:
    return await create_user_interactor(create_user_request)


@user_router.delete('/{user_id}', summary='Delete user by telegram id')
async def delete_user(
    user_id: int,
    delete_user_interactor: FromDishka[DeleteUser],
) -> None:
    return await delete_user_interactor(user_id)


@user_router.get('', summary='Get a list of users', response_model=list[UserDB])
async def get_users(
    get_users_interactor: FromDishka[GetAllUsers],
) -> list[UserDB]:
    return await get_users_interactor()


@user_router.get(
    '/{user_id}',
    summary='Get a user by telegram id',
    response_model=GetUserResponse,
)
async def get_user(user_id: int, get_user_interactor: FromDishka[GetUserByTelegramId]) -> GetUserResponse:
    return await get_user_interactor(user_id)


@user_router.get(
    '/{user_id}/requests',
    summary='Get user limits',
    response_model=list[GetUserRequestsResponse],
)
async def get_user_requests(
    user_id: uuid.UUID, get_user_requests_interactor: FromDishka[GetUserRequests]
) -> list[GetUserRequestsResponse]:
    return await get_user_requests_interactor(user_id)


@user_router.put('/{user_id}/requests', summary='Update user limits')
async def update_user_requests(
    user_id: uuid.UUID,
    model_name: str,
    amount: int,
    update_user_requests_interactor: FromDishka[UpdateUserRequests],
) -> None:
    return await update_user_requests_interactor(user_id, model_name, amount)


@user_router.get(
    '/{user_id}/subscription',
    summary='Get a user subscription',
    response_model=GetUserSubscriptionResponse | None,
)
async def get_user_subscription(
    user_id: uuid.UUID,
    get_user_subscriptions_interactor: FromDishka[GetUserSubscription],
) -> GetUserSubscriptionResponse:
    return await get_user_subscriptions_interactor(user_id)


@user_router.get(
    '/{user_id}/subscriptions',
    summary='Get all user subscriptions',
    response_model=list[GetUserSubscriptionResponse],
)
async def get_user_subscriptions(
    user_id: uuid.UUID,
    get_user_subscriptions_interactor: FromDishka[GetUserSubscriptions],
) -> list[GetUserSubscriptionResponse]:
    return await get_user_subscriptions_interactor(user_id)


@user_router.put('/{user_id}/subscription', summary='Change user subscription')
async def update_user_subscription(
    user_id: uuid.UUID,
    subscription_name: str,
    change_user_subscription_interactor: FromDishka[UpdateUserSubscription],
) -> None:
    return await change_user_subscription_interactor(user_id, subscription_name)
