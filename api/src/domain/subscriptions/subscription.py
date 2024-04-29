import uuid
from dataclasses import dataclass


@dataclass
class Subscription:
    id: uuid.UUID
    name: str

    @staticmethod
    def create(name: str) -> "Subscription":
        return Subscription(
            id=uuid.uuid4(),
            name=name,
        )
