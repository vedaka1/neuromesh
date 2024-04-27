import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.neural_networks.model import Model


@dataclass
class BaseNeuralNetworkRepository(ABC):
    @abstractmethod
    async def create(self, model: Model) -> None: ...

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Model | None: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Model | None: ...

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Model] | None: ...

    @abstractmethod
    async def get_all_by_subscription_id(
        self, subscription_id: uuid.UUID, limit: int = 10, offset: int = 0
    ) -> list[Model] | None: ...

    @abstractmethod
    async def update_requests_amount(
        self, id: uuid.UUID, requests_amount: int
    ) -> Model | None: ...
