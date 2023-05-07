from dataclasses import dataclass
from typing import TypeVar, Iterable, List, Tuple, Union

from marshy.types import ExternalItemType, ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC

T = TypeVar("T")


@dataclass(frozen=True)
class TupleMarshaller(MarshallerABC[Iterable[T]]):
    """
    Marshaller for iterable types (lists)
    """

    item_marshallers: Tuple[MarshallerABC[T], ...]

    def load(self, item: Union[List[ExternalType], ExternalItemType]) -> Iterable[T]:
        if isinstance(item, dict):
            loaded = tuple(
                m.load(item[f"t{i}"]) for i, m in enumerate(self.item_marshallers)
            )
            return loaded
        loaded = tuple(m.load(i) for m, i in zip(self.item_marshallers, item))
        return loaded

    def dump(self, item: Iterable[T]) -> List[ExternalType]:
        dumped = [m.dump(i) for m, i in zip(self.item_marshallers, item)]
        return dumped
