from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from marshy.types import ExternalType

T = TypeVar('T')


@dataclass(frozen=True)
class MarshallerABC(ABC, Generic[T]):
    marshalled_type: Type[T]

    @abstractmethod
    def load(self, item: ExternalType) -> T:
        """ Marshall the object given """

    @abstractmethod
    def dump(self, item: T) -> ExternalType:
        """ Unmarshall the object given """
