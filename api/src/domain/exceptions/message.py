from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False, init=False)
class MessageTooLongException(ApplicationException):
    message: str = "Message too long"


@dataclass(eq=False, init=False)
class EmptyMessageException(ApplicationException):
    message: str = "Message cannot be empty"
