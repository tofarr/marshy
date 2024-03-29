from dataclasses import dataclass
from typing import TypeVar, Type

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.marshy_context import MarshyContext

T = TypeVar("T")


@dataclass(frozen=True)
class DeferredMarshaller(MarshallerABC[T]):
    marshalled_type: Type[T]
    marshaller_context: MarshyContext

    def get_marshaller(self) -> MarshallerABC[T]:
        marshaller = self.marshaller_context.get_marshaller(self.marshalled_type)
        return marshaller

    def load(self, item: ExternalType) -> T:
        loaded = self.get_marshaller().load(item)
        return loaded

    def dump(self, item: T) -> ExternalType:
        dumped = self.get_marshaller().dump(item)
        return dumped
