from dataclasses import dataclass

from application.common.transaction import BaseTransactionManager
from domain.users.repository import BaseUserRepository
from domain.users.user import User


@dataclass
class GetAllUsers:
    user_repository: BaseUserRepository
    transaction_manager: BaseTransactionManager

    async def __call__(self) -> list[User]:
        result = await self.user_repository.get_all()
        await self.transaction_manager.close()
        return result
