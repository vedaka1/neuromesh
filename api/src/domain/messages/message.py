from dataclasses import dataclass

from domain.common.value import ValueObject
from domain.exeptions.message import EmptyMessageExeption, MessageTooLongExeption


@dataclass
class Message(ValueObject):
    value: str

    def __post_init__(self):
        if len(self.value) > 1000:
            raise MessageTooLongExeption()
        if not self.value:
            raise EmptyMessageExeption()
