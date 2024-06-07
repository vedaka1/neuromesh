from dataclasses import dataclass

from domain.users.repository import BaseUserRepository
from domain.users.user import User


@dataclass
class GetAllUsers:
    user_repository: BaseUserRepository

    async def __call__(self) -> list[User]:
        result = await self.user_repository.get_all()
        return result
