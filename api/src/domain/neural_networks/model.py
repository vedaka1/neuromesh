import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import Logger
from typing import Any, Generic, TypeVar


@dataclass
class BaseTextModel(ABC):
    logger: Logger

    @abstractmethod
    async def generate_response(
        self, user_id: uuid.UUID, message: str
    ) -> str | None: ...
    @abstractmethod
    @staticmethod
    def create_message(message: str) -> dict[str, str]: ...


@dataclass
class BaseImageModel(ABC):

    @abstractmethod
    async def generate_response(self, user_prompt: str) -> dict[str, Any] | None: ...


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
    subscription_name: str
    requests: int

    @staticmethod
    def create(
        model_name: str, subscription_name: str, requests: int
    ) -> "ModelSubscription":
        return ModelSubscription(
            id=uuid.uuid4(),
            neural_network_name=model_name,
            subscription_name=subscription_name,
            requests=requests,
        )
