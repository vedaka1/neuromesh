from dataclasses import dataclass


@dataclass
class ModelSubscriptionResponse:
    name: str
    requests: int


@dataclass
class GetSubscriptionResponse:
    name: str
    models: list[ModelSubscriptionResponse]
