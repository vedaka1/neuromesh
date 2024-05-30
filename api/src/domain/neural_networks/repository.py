import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.neural_networks.model import Model, ModelSubscription


@dataclass
class BaseNeuralNetworkRepository(ABC):
    @abstractmethod
    async def create(self, model: Model) -> None: ...

    @abstractmethod
    async def delete(self, name: str) -> None: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Model | None: ...

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Model] | None: ...


@dataclass
class BaseNeuralNetworkSubscriptionRepository(ABC):
    @abstractmethod
    async def create(self, model_subscription: ModelSubscription) -> None: ...

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> ModelSubscription: ...

    @abstractmethod
    async def get_all_by_subscription_name(
        self, subscription_name: str
    ) -> list[ModelSubscription] | None: ...

    @abstractmethod
    async def get_all(
        self, limit: int = 10, offset: int = 0
    ) -> list[ModelSubscription] | None: ...
