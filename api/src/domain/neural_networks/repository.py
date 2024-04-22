from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseNeuralNetworkRepository(ABC):
    @abstractmethod
    async def create(self) -> None: ...

    @abstractmethod
    async def delete(self) -> None: ...

    @abstractmethod
    async def get_by_id(self) -> None: ...

    @abstractmethod
    async def get_all(self) -> None: ...

    @abstractmethod
    async def update_requests_amount(self) -> None: ...
