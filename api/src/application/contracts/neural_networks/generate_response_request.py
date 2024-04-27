import uuid
from dataclasses import dataclass

from domain.messages.message import Message


@dataclass
class GenerateResponseRequest:
    model: str
    user_id: uuid.UUID
    message: str
