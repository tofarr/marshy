from dataclasses import dataclass
from typing import TypeVar, Iterable, List, Tuple

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC

T = TypeVar('T')


@dataclass(frozen=True)
class TupleMarshaller(MarshallerABC[Iterable[T]]):
    """
    Marshaller for iterable types (lists)
    """
    item_marshallers: Tuple[MarshallerABC[T], ...]

    def load(self, item: List[ExternalType]) -> Iterable[T]:
        loaded = tuple(m.load(i) for m, i in zip(self.item_marshallers, item))
        return loaded

    def dump(self, item: Iterable[T]) -> List[ExternalType]:
        dumped = [m.dump(i) for m, i in zip(self.item_marshallers, item)]
        return dumped
