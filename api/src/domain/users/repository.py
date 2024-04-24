from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseUserRepository(ABC):
    @abstractmethod
    async def create(self) -> None: ...

    @abstractmethod
    async def delete(self) -> None: ...

    @abstractmethod
    async def get_by_telegram_id(self) -> None: ...

    @abstractmethod
    async def get_all(self) -> None: ...

    @abstractmethod
    async def update_subscription(self) -> None: ...


@dataclass
class BaseUserSubscriptionRepository(ABC):
    @abstractmethod
    async def create(self) -> None: ...

    @abstractmethod
    async def delete(self) -> None: ...

    @abstractmethod
    async def get_by_telegram_id(self) -> None: ...

    @abstractmethod
    async def get_all(self) -> None: ...

    @abstractmethod
    async def update(self) -> None: ...


@dataclass
class BaseUserRequestRepository(ABC):
    @abstractmethod
    async def create(self) -> None: ...

    @abstractmethod
    async def delete(self) -> None: ...

    @abstractmethod
    async def get_by_id(self) -> None: ...

    @abstractmethod
    async def get_all_by_user_id(self) -> None: ...

    @abstractmethod
    async def update(self) -> None: ...
