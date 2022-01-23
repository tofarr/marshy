from abc import ABC, abstractmethod
from functools import total_ordering
from typing import Optional, Type

_MarshallerContext = 'marshy.marshaller_context.MarshallerContext'
_MarshallerABC = 'marshy.marshaller_abc.MarshallerABC'


@total_ordering
class MarshallerFactoryABC(ABC):

    @property
    def priority(self) -> int:
        return 0

    def __ne__(self, other):
        return self.priority != getattr(other, 'priority', None)

    def __lt__(self, other):
        return self.priority < getattr(other, 'priority', None)

    @abstractmethod
    def create(self,
               context: _MarshallerContext,
               type_: Type) -> Optional[_MarshallerABC]:
        """
        Create a new marshaller instance if possible - if not return None
        """
