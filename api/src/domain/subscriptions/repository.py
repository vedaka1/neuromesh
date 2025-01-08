from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.subscriptions.subscription import Subscription


@dataclass
class BaseSubscriptionRepository(ABC):
    @abstractmethod
    async def create(self, subscription: Subscription) -> None: ...

    @abstractmethod
    async def delete(self, name: str) -> None: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Subscription | None: ...

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Subscription]: ...

    @abstractmethod
    async def update(self, name: str) -> None: ...
