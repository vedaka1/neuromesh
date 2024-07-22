import uuid
from dataclasses import dataclass
from typing import Optional

from application.contracts.users.get_user_requests import GetUserRequestsResponse
from application.contracts.users.get_user_subscriptions_response import (
    GetUserSubscriptionResponse,
)


@dataclass
class GetUserResponse:
    id: uuid.UUID
    telegram_id: int
    username: str
    subscription: GetUserSubscriptionResponse
    requests: list[GetUserRequestsResponse]
