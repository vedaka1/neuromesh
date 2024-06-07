from dataclasses import dataclass

from domain.exeptions.base import ApplicationException


@dataclass(eq=False, init=False)
class GenerationException(ApplicationException):
    message: str = "Error during generation"
