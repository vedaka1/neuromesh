from dataclasses import dataclass


@dataclass
class RegisterRequest:
    telegram_id: int
    username: str
