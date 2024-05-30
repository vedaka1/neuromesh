import uuid
from dataclasses import dataclass

from domain.subscriptions.subscription import Subscription
from domain.users.user import UserRequest


@dataclass
class GetUserResponse:
    id: uuid.UUID
    telegram_id: int
    username: str
    subscription: Subscription
    requests: list[UserRequest]
