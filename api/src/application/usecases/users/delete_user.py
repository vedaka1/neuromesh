from dataclasses import dataclass

from application.common.transaction import ICommiter
from domain.users.repository import BaseUserRepository


@dataclass
class DeleteUser:
    user_repository: BaseUserRepository
    commiter: ICommiter

    async def __call__(self, user_id: int) -> None:
        await self.user_repository.delete(user_id)
        await self.commiter.commit()
