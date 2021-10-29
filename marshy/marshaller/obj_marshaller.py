from dataclasses import dataclass
from typing import TypeVar, Tuple, Optional

from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalType

T = TypeVar('T')


@dataclass(frozen=True)
class AttrConfig:
    internal_name: str
    external_name: str
    marshaller: MarshallerABC
    load: bool
    dump: bool
    exclude_dumped_values: Tuple = (None,)


def attr_config(marshaller: MarshallerABC,
                internal_name: str,
                external_name: Optional[str] = None,
                load: bool = True,
                dump: bool = True,
                exclude_dumped_values: Tuple = tuple()) -> AttrConfig:
    if external_name is None:
        external_name = internal_name
    return AttrConfig(internal_name, external_name, marshaller, load, dump, exclude_dumped_values)


@dataclass(frozen=True)
class ObjMarshaller(MarshallerABC[T]):
    attr_configs: Tuple

    def load(self, item: ExternalType) -> T:
        kwargs = {}
        for a in self.attr_configs:
            if a.load:
                external_value = item.get(a.external_name)
                value = a.marshaller.load(external_value)
                kwargs[a.internal_name] = value
        loaded = self.marshalled_type(**kwargs)
        return loaded

    def dump(self, item: T) -> ExternalType:
        if hasattr(item, 'get'):
            def getter(obj, key):
                return obj.get(key)
        else:
            getter = getattr

        dumped = {}
        for a in self.attr_configs:
            if a.dump:
                value = getter(item, a.internal_name)
                if value not in a.exclude_dumped_values:
                    external_value = a.marshaller.dump(value)
                    dumped[a.external_name] = external_value
        return dumped
