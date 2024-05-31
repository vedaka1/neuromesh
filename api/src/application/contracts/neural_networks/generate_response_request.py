import uuid
from dataclasses import dataclass


@dataclass
class GenerateResponseRequest:
    model: str
    user_id: uuid.UUID
    message: str
