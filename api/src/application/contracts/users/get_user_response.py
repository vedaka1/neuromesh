import uuid
from dataclasses import dataclass


@dataclass
class GetUserResponse:
    id: uuid.UUID
    telegram_id: int
    username: str
    is_subscribed: uuid.UUID
