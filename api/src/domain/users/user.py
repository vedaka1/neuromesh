from dataclasses import dataclass, field

from domain.ai.model import BaseTextModel


@dataclass
class UserDB:
    telegram_id: int
    username: str
    is_premium: bool = field(default=False, init=False)


@dataclass
class User(UserDB):
    messages: list[dict] = field(default_factory=list, init=False)
    model: BaseTextModel = field(default=None, init=False)
