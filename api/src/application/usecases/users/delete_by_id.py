from dataclasses import dataclass

from application.common.transaction import BaseTransactionManager
from domain.users.repository import BaseUserRepository


@dataclass
class DeleteUser:
    user_repository: BaseUserRepository

    transaction_manager: BaseTransactionManager

    async def __call__(self, user_id: int) -> None:
        await self.user_repository.delete(user_id)

        await self.transaction_manager.commit()
        await self.transaction_manager.close()
