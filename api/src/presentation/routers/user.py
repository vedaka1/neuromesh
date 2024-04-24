from fastapi import APIRouter, Depends
from punq import Container

from application.contracts.users.get_user_response import GetUserResponse
from application.contracts.users.register_request import RegisterRequest
from application.usecases.user import UserService
from infrastructure.di.container import get_container

user_router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@user_router.get("/", response_model=GetUserResponse)
async def create_user(
    create_user_request: RegisterRequest,
    container: Container = Depends(get_container),
):
    user_service: UserService = container.resolve(UserService)
    return await user_service.create_user(create_user_request)
