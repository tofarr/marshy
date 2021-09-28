from dataclasses import dataclass
from typing import TypeVar, Dict

from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalType

T = TypeVar('T')


@dataclass(frozen=True)
class ObjMarshaller(MarshallerABC[T]):
    attr_marshallers: Dict[str, MarshallerABC]
    filter_none: bool = True

    def load(self, item: ExternalType) -> T:
        kwargs = {k: m.load(item.get(k)) for k, m in self.attr_marshallers.items() if k in item}
        loaded = self.marshalled_type(**kwargs)
        return loaded

    def dump(self, item: T) -> ExternalType:
        if hasattr(item, 'get'):
            def getter(obj, key):
                return obj.get(key)
        else:
            getter = getattr

        dumped = {k: m.dump(getter(item, k)) for k, m in self.attr_marshallers.items()}
        if self.filter_none:
            dumped = {k: v for k, v in dumped.items() if v is not None}
        return dumped
