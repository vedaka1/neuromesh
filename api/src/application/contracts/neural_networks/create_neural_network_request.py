import uuid
from dataclasses import dataclass


@dataclass
class CreateNeuralNetworkRequest:
    name: str
