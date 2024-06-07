import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import Logger
from typing import TypeVar

LT = TypeVar("LT", bound=Logger)


@dataclass
class BaseTextModel(ABC):
    logger: LT

    @abstractmethod
    def create_message(self) -> dict[str, str]: ...

    @abstractmethod
    async def generate_response(self) -> str | None: ...


@dataclass
class Model:
    name: str

    @staticmethod
    def create(name: str) -> "Model":
        return Model(
            name=name,
        )


@dataclass
class ModelSubscription:
    id: uuid.UUID
    neural_network_name: str
    subscription_name: uuid.UUID
    requests: int

    @staticmethod
    def create(
        model_name: uuid.UUID, subscription_name: uuid.UUID, requests: int
    ) -> "ModelSubscription":
        return ModelSubscription(
            id=uuid.uuid4(),
            neural_network_name=model_name,
            subscription_name=subscription_name,
            requests=requests,
        )
