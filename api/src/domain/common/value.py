from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

VT = TypeVar("VT", bound=Any)


@dataclass
class ValueObject(ABC, Generic[VT]):
    value: VT
