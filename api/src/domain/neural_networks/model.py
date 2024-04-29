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
    def create_message(self) -> None: ...

    @abstractmethod
    async def generate_response(self) -> None: ...


@dataclass
class Model:
    id: uuid.UUID
    name: str

    @staticmethod
    def create(name: str) -> "Model":
        return Model(
            id=uuid.uuid4(),
            name=name,
        )


@dataclass
class ModelSubscription:
    id: uuid.UUID
    neural_network_id: uuid.UUID
    subscription_id: uuid.UUID
    requests: int

    @staticmethod
    def create(
        model_id: uuid.UUID, subscription_id: uuid.UUID, requests: int
    ) -> "ModelSubscription":
        return ModelSubscription(
            id=uuid.uuid4(),
            neural_network_id=model_id,
            subscription_id=subscription_id,
            requests=requests,
        )
