from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseModelManager(ABC):
    @abstractmethod
    async def generate_response(self, user_id, model_name, message) -> str: ...
