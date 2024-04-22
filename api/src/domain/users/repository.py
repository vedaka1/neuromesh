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
class BaseUserSubscriptionsRepository(ABC):
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
class BaseUserRequestsRepository(ABC):
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
