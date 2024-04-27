import uuid
from dataclasses import dataclass


@dataclass
class CreateNeuralNetworkRequest:
    subscription_id: uuid.UUID
    name: str
    requests_amount: int
