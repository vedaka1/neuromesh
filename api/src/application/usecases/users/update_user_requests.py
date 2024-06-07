import uuid
from dataclasses import dataclass

from application.common.transaction import BaseTransactionManager
from domain.users.repository import BaseUserRepository, BaseUserRequestRepository
from fastapi import HTTPException


@dataclass
class UpdateUserRequests:
    user_repository: BaseUserRepository
    user_requests_repository: BaseUserRequestRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, user_id: uuid.UUID, amount: int) -> None:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await self.user_requests_repository.update_user_requests(user_id, amount)

        await self.transaction_manager.commit()
