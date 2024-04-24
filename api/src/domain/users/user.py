import datetime
import uuid
from dataclasses import dataclass, field

from domain.neural_networks.model import BaseTextModel


@dataclass
class UserDB:
    id: uuid.UUID
    telegram_id: int
    username: str
    is_subscribed: bool = False

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


@dataclass
class UserSubscription:
    id: uuid.UUID
    user_id: uuid.UUID
    subscription_id: uuid.UUID
    created_at: datetime
    expires_in: int

    @staticmethod
    def create(
        user_id: uuid.UUID, subscription_id: uuid.UUID, expires_in: int = 30
    ) -> "UserSubscription":
        return UserSubscription(
            id=uuid.uuid4(),
            user_id=user_id,
            subscription_id=subscription_id,
            expires_in=expires_in,
        )


@dataclass
class UserRequest:
    id: uuid.UUID
    user_id: uuid.UUID
    neural_network_id: uuid.UUID
    amount: int

    @staticmethod
    def create(
        user_id: uuid.UUID, neural_network_id: uuid.UUID, amount: int
    ) -> "UserRequest":
        return UserRequest(
            id=uuid.uuid4(),
            user_id=user_id,
            neural_network_id=neural_network_id,
            amount=amount,
        )
