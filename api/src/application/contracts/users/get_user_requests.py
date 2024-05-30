from dataclasses import dataclass


@dataclass
class GetUserRequests:
    neural_network_name: str
    amount: int
