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
    async def generate_response(self) -> str: ...
