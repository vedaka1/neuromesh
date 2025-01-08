from dataclasses import dataclass


@dataclass
class Subscription:
    name: str

    @staticmethod
    def create(name: str) -> 'Subscription':
        return Subscription(name=name)
