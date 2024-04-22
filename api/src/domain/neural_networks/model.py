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
    subscription_id: int
    name: str
    requests_amount: int

    @staticmethod
    def create(subscription_id: uuid.UUID, name: str, requests_amount: int) -> "Model":
        return Model(
            id=uuid.uuid4(),
            subscription_id=subscription_id,
            name=name,
            requests_amount=requests_amount,
        )
