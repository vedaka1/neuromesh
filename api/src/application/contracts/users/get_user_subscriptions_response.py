import datetime
from dataclasses import dataclass


@dataclass
class GetUserSubscriptionResponse:
    subscription_name: str
    created_at: datetime.datetime | None
    expires_in: datetime.datetime | None
