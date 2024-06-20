import datetime
from dataclasses import dataclass


@dataclass
class GetUserSubscriptionResponse:
    subscription_name: str
    created_at: datetime.datetime
    expires_in: int
    is_expired: bool
