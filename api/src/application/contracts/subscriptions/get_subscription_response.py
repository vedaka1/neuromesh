import uuid
from dataclasses import dataclass

from domain.neural_networks.model import Model


@dataclass
class GetSubscriptionResponse:
    name: str
    models: list[Model]
