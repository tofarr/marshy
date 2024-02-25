from abc import ABC, abstractmethod
from functools import total_ordering
from typing import Optional, Type

_MarshyContext = "marshy.marshy_context.MarshyContext"
_MarshallerABC = "marshy.marshaller_abc.MarshallerABC"


@total_ordering
class MarshallerFactoryABC(ABC):
    priority: int = 0

    @abstractmethod
    def create(self, context: _MarshyContext, type_: Type) -> Optional[_MarshallerABC]:
        """
        Create a new marshaller instance if possible, otherwise return None
        """

    def __ne__(self, other):
        return self.priority != getattr(other, "priority", None)

    def __lt__(self, other):
        return self.priority < getattr(other, "priority", None)
