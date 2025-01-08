from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False, init=False)
class UserNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = 'User not found'


@dataclass(eq=False, init=False)
class UserAlreadyExistsException(ApplicationException):
    status_code: int = 400
    message: str = 'User already exists'


@dataclass(eq=False, init=False)
class UserAlreadySubscribedException(ApplicationException):
    status_code: int = 400
    message: str = 'User already subscribed'
