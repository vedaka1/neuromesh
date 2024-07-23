from dataclasses import dataclass
from typing import ClassVar

from domain.exceptions.base import ApplicationException


@dataclass(eq=False, init=False)
class GenerationException(ApplicationException):
    message: ClassVar[str] = "Error during generation"


@dataclass(eq=False, init=False)
class ModelUnavailableException(ApplicationException):
    status_code: int = 503
    message: ClassVar[str] = "Model currently unavailable"


@dataclass(eq=False, init=False)
class ModelNotFoundException(ApplicationException):
    status_code: int = 404
    message: ClassVar[str] = "Model not found"


@dataclass(eq=False, init=False)
class ModelAlreadyExistsException(ApplicationException):
    status_code: int = 400
    message: ClassVar[str] = "Model already exists"


@dataclass(eq=False, init=False)
class ModelAlreadyInSubscriptionException(ApplicationException):
    status_code: int = 400
    message: ClassVar[str] = "Model already added to subscription"


@dataclass(eq=False, init=False)
class NoAccessToModelException(ApplicationException):
    status_code: int = 403
    message: ClassVar[str] = "You don't have access to this model"
