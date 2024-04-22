import uuid
from dataclasses import dataclass, field

from domain.neural_networks.model import BaseTextModel


@dataclass
class UserDB:
    id: uuid.UUID
    telegram_id: int
    username: str
    subscription: uuid.UUID | None = field(default=None)

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
