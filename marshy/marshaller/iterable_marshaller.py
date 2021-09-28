from dataclasses import dataclass
from typing import TypeVar, Iterable, List

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC

T = TypeVar('T')


@dataclass(frozen=True)
class IterableMarshaller(MarshallerABC[Iterable[T]]):
    """
    Marshaller for iterable types (lists)
    """
    item_marshaller: MarshallerABC[T]

    def load(self, item: List[ExternalType]) -> Iterable[T]:
        loaded = [self.item_marshaller.load(i) for i in item]
        return loaded

    def dump(self, item: Iterable[T]) -> List[ExternalType]:
        dumped = [self.item_marshaller.dump(i) for i in item]
        return dumped
