from dataclasses import dataclass


@dataclass
class CreateSubscriptionRequest:
    name: str
    validity_period: int
