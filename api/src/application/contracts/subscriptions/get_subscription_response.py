import uuid
from dataclasses import dataclass

from domain.neural_networks.model import Model


@dataclass
class GetSubscriptionResponse:
    id: uuid.UUID
    name: str
    models: list[Model]
