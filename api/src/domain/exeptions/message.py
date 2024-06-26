from dataclasses import dataclass

from domain.exeptions.base import ApplicationException


@dataclass(eq=False, init=False)
class MessageTooLongException(ApplicationException):
    message: str = "Message too long"


@dataclass(eq=False, init=False)
class EmptyMessageException(ApplicationException):
    message: str = "Message cannot be empty"
