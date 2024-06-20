from dataclasses import dataclass


@dataclass
class GetUserRequestsResponse:
    neural_network_name: str
    amount: int
