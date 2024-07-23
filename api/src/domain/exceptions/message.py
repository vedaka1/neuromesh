from dataclasses import dataclass
from typing import ClassVar

from domain.exceptions.base import ApplicationException


@dataclass(eq=False, init=False)
class MessageTooLongException(ApplicationException):
    message: ClassVar[str] = "Message too long"


@dataclass(eq=False, init=False)
class EmptyMessageException(ApplicationException):
    message: ClassVar[str] = "Message cannot be empty"
