from dataclasses import dataclass

from domain.common.value import ValueObject
from domain.exeptions.message import EmptyMessageException, MessageTooLongException


@dataclass
class Message(ValueObject[str]):
    value: str

    def __post_init__(self):
        if len(self.value) > 1000:
            raise MessageTooLongException()
        if not self.value:
            raise EmptyMessageException()
