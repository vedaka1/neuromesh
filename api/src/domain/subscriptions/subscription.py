import uuid
from dataclasses import dataclass


@dataclass
class Subscription:
    id: uuid.UUID
    name: str
    validity_period: int

    @staticmethod
    def create(name: str, validity_period: int) -> "Subscription":
        return Subscription(
            id=uuid.uuid4(),
            name=name,
            validity_period=validity_period,
        )
