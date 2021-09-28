from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import total_ordering
from typing import Optional, Type

MarshallerContext = 'marshy.marshaller_context.MarshallerContext'
MarshallerABC = 'marshy.marshaller_abc.MarshallerABC'


@dataclass
@total_ordering
class MarshallerFactoryABC(ABC):
    priority: int = 0

    def __ne__(self, other):
        return self.priority != getattr(other, 'priority', None)

    def __lt__(self, other):
        return self.priority < getattr(other, 'priority', None)

    @abstractmethod
    def create(self,
               context: MarshallerContext,
               type_: Type) -> Optional[MarshallerABC]:
        """
        Create a new marshaller instance if possible - if not return None
        """
