from dataclasses import dataclass
from typing import TypeVar

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.marshaller_context import MarshallerContext

T = TypeVar('T')


@dataclass(frozen=True)
class DeferredMarshaller(MarshallerABC[T]):
    marshaller_context: MarshallerContext

    def get_marshaller(self) -> MarshallerABC[T]:
        marshaller = self.marshaller_context.get_marshaller(self.marshalled_type)
        return marshaller

    def load(self, item: ExternalType) -> T:
        loaded = self.get_marshaller().load(item)
        return loaded

    def dump(self, item: T) -> ExternalType:
        dumped = self.get_marshaller().dump(item)
        return dumped
