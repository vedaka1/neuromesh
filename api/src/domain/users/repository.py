import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.users.user import User, UserDB, UserRequest, UserSubscription


@dataclass
class BaseUserRepository(ABC):
    @abstractmethod
    async def create(self, user: UserDB) -> None: ...

    @abstractmethod
    async def delete(self, telegram_id: int) -> None: ...

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> UserDB: ...

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> UserDB: ...

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[UserDB]: ...

    @abstractmethod
    async def update_subscription(
        self, user_id: uuid.UUID, subscription_id: bool
    ) -> UserDB: ...


@dataclass
class BaseUserSubscriptionRepository(ABC):
    @abstractmethod
    async def create(
        self, user_subscription: UserSubscription
    ) -> UserSubscription | None: ...

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> UserSubscription | None: ...

    @abstractmethod
    async def get_all(
        self, limit: int = 10, offset: int = 0
    ) -> list[UserSubscription] | None: ...

    @abstractmethod
    async def get_by_user_id(
        self, user_id: uuid.UUID, limit: int = 10, offset: int = 0
    ) -> list[UserSubscription] | None: ...

    @abstractmethod
    async def update(self, id: uuid.UUID, expires_in: int) -> None: ...


@dataclass
class BaseUserRequestRepository(ABC):
    @abstractmethod
    async def create(self, user_request: UserRequest) -> None: ...

    @abstractmethod
    async def delete_user_requests(self, id: uuid.UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> UserRequest | None: ...

    @abstractmethod
    async def get_all_by_user_id(
        self, user_id: uuid.UUID, limit: int = 10, offset: int = 0
    ) -> list[UserRequest] | None: ...

    @abstractmethod
    async def get_by_user_and_model_id(
        self, model_id: uuid.UUID, user_id: uuid.UUID
    ) -> UserRequest | None: ...

    @abstractmethod
    async def update_user_requests(self, user_id: uuid.UUID, amount: int) -> None: ...
