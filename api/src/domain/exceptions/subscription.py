from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False, init=False)
class SubscriptionNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "Subscription not found"


@dataclass(eq=False, init=False)
class SubscriptionExpiredException(ApplicationException):
    status_code: int = 403
    message: str = "Subscription expired"


@dataclass(eq=False, init=False)
class SubscriptionAlreadyExistsException(ApplicationException):
    status_code: int = 400
    message: str = "Subscription already exists"
