import uuid
from dataclasses import dataclass, field

from domain.ai.model import BaseTextModel


@dataclass
class UserDB:
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    telegram_id: int
    username: str
    is_premium: bool = field(default=False, init=False)


@dataclass
class User(UserDB):
    messages: list[dict] = field(default_factory=list, init=False)
    model: BaseTextModel = field(default=None, init=False)
