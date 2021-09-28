from typing import Type, Optional, Dict, Any

from marshy.errors import MarshallError
from marshy.factory import marshaller_factory_abc
from marshy.marshaller import marshaller_abc
from marshy.types import ExternalType
from marshy.utils import resolve_forward_refs


class MarshallerContext:

    def __init__(self,
                 factories: Optional[marshaller_factory_abc.MarshallerFactoryABC] = None,
                 by_type: Optional[Dict[Type, marshaller_abc.MarshallerABC]] = None):
        self._factories = sorted(factories or [], reverse=True)
        self._by_type = dict(by_type or {})

    def register_factory(self, marshaller_factory: marshaller_factory_abc.MarshallerFactoryABC):
        self._factories.append(marshaller_factory)
        self._factories = sorted(self._factories or [], reverse=True)

    def register_marshaller(self, marshaller: marshaller_abc.MarshallerABC, type_: Type = None):
        type_ = type_ or marshaller.marshalled_type
        self._by_type[type_] = marshaller

    def get_marshaller(self, type_: Type) -> marshaller_abc.MarshallerABC:
        marshaller = self._by_type.get(type_)
        if not marshaller:
            resolved_type = resolve_forward_refs(type_)
            for factory in self._factories:
                marshaller = factory.create(self, resolved_type)
                if marshaller:
                    break
            if not marshaller:
                raise MarshallError(f'NoMarshallerForType:{type_}')
            self._by_type[type_] = marshaller
        return marshaller

    def load(self, type_: Type, to_load: ExternalType):
        marshaller = self.get_marshaller(type_)
        loaded = marshaller.load(to_load)
        return loaded

    def dump(self, obj: Any, type_: Optional[Type] = None) -> ExternalType:
        if not type_:
            type_ = type(obj)
        marshaller = self.get_marshaller(type_)
        dumped = marshaller.dump(obj)
        return dumped
