import datetime
import uuid
from dataclasses import dataclass, field

from domain.neural_networks.model import BaseTextModel


@dataclass
class UserDB:
    id: uuid.UUID
    telegram_id: int
    username: str
    current_subscription: str = 'Free'

    @staticmethod
    def create(telegram_id: int, username: str) -> 'UserDB':
        return UserDB(
            id=uuid.uuid4(),
            telegram_id=telegram_id,
            username=username,
        )


@dataclass
class User(UserDB):
    messages: list[dict] = field(default_factory=list, init=False)
    model: BaseTextModel = field(default_factory=BaseTextModel, init=False)


@dataclass
class UserSubscription:
    id: uuid.UUID
    user_id: uuid.UUID
    subscription_name: str
    created_at: datetime.datetime
    expires_in: datetime.datetime
    is_expired: bool

    @staticmethod
    def create(
        user_id: uuid.UUID,
        subscription_name: str,
        expires_in: int = 30,
    ) -> 'UserSubscription':
        return UserSubscription(
            id=uuid.uuid4(),
            user_id=user_id,
            subscription_name=subscription_name,
            created_at=datetime.datetime.now(),
            expires_in=datetime.datetime.now() + datetime.timedelta(days=expires_in),
            is_expired=False,
        )


@dataclass
class UserRequest:
    id: uuid.UUID
    user_id: uuid.UUID
    neural_network_name: str
    amount: int

    @staticmethod
    def create(user_id: uuid.UUID, neural_network_name: str, amount: int) -> 'UserRequest':
        return UserRequest(
            id=uuid.uuid4(),
            user_id=user_id,
            neural_network_name=neural_network_name,
            amount=amount,
        )
