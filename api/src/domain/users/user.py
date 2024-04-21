import uuid
from dataclasses import dataclass, field

from domain.ai.model import BaseTextModel


@dataclass
class UserDB:
    id: uuid.UUID
    telegram_id: int
    username: str
    subscripion: uuid.UUID | None = field(default=None, init=False)

    @staticmethod
    def create(telegram_id: int, username: str) -> "UserDB":
        return UserDB(
            id=uuid.uuid4(),
            telegram_id=telegram_id,
            username=username,
        )


@dataclass
class User(UserDB):
    messages: list[dict] = field(default_factory=list, init=False)
    model: BaseTextModel = field(default=None, init=False)
