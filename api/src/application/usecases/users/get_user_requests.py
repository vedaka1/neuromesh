import uuid
from dataclasses import dataclass

from fastapi import HTTPException

from application.common.transaction import BaseTransactionManager
from domain.users.repository import BaseUserRepository, BaseUserRequestRepository
from domain.users.user import UserRequest


@dataclass
class GetUserRequests:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, user_id: uuid.UUID) -> list[UserRequest]:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        requests = await self.user_requests_repository.get_all_by_user_id(user_id)

        await self.transaction_manager.close()

        return requests
