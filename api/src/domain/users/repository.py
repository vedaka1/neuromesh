import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.users.user import User


@dataclass
class BaseUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> None: ...

    @abstractmethod
    async def delete(self, telegram_id: int) -> None: ...

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> User: ...

    @abstractmethod
    async def update_subscription(self, telegram_id: int, subscription) -> None: ...
