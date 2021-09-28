from dataclasses import dataclass
from typing import TypeVar, Tuple

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

T = TypeVar('T')


@dataclass(frozen=True)
class PropertyConfig:
    external_name: str
    marshaller: MarshallerABC
    prop: property
    load: bool = True
    dump: bool = True
    filter_dumped_values: Tuple = (None,)


class PropertyMarshaller(MarshallerABC[T]):
    """
    Marshaller which wraps another and uses property setters / getters.
    """
    # noinspection PyDataclass
    def __init__(self, marshaller: MarshallerABC[T], property_configs: Tuple[PropertyConfig]):
        super().__init__(marshaller.marshalled_type)
        self.marshaller = marshaller
        self.property_configs = property_configs

    def load(self, item: ExternalItemType) -> T:
        loaded = self.marshaller.load(item)
        for property_config in self.property_configs:
            if property_config.load:
                external_value = item.get(property_config.external_name)
                value = property_config.marshaller.load(external_value)
                property_config.prop.fset(loaded, value)
        return loaded

    def dump(self, item: T) -> ExternalType:
        dumped: ExternalItemType = self.marshaller.dump(item)
        for property_config in self.property_configs:
            if property_config.dump:
                value = property_config.prop.fget(item)
                if value not in property_config.filter_dumped_values:
                    external_value = property_config.marshaller.dump(value)
                    dumped[property_config.external_name] = external_value
        return dumped
