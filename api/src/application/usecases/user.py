from dataclasses import dataclass

from fastapi.exceptions import HTTPException

from application.contracts.users.get_user_response import GetUserResponse
from application.contracts.users.register_request import RegisterRequest
from domain.users.user import UserDB
from infrastructure.persistence.repositories.user import UserRepository


@dataclass
class UserService:
    user_repository: UserRepository

    @classmethod
    async def create_user(cls, request: RegisterRequest) -> GetUserResponse:
        user_exists = await cls.user_repository.get_by_telegram_id(request.telegram_id)

        if user_exists:
            raise HTTPException(status_code=400, detail="User already exists")

        user = UserDB.create(telegram_id=request.telegram_id, username=request.username)
        await cls.user_repository.create(user)

        return GetUserResponse(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
        )

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> GetUserResponse:
        user = await cls.user_repository.get_by_telegram_id(user_id)

        return GetUserResponse(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
        )
