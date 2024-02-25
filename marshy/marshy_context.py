from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type, TypeVar

from injecty import InjectyContext, get_default_injecty_context

from marshy.errors import MarshallError
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.utils import resolve_forward_refs
from marshy.types import ExternalType

T = TypeVar("T")


@dataclass
class MarshyContext:
    marshallers_by_type: Dict[Type, MarshallerABC] = field(default_factory=dict)
    factories: List[MarshallerFactoryABC] = field(default_factory=list)
    injecty_context: Optional[InjectyContext] = field(
        default_factory=get_default_injecty_context
    )

    def load(self, type_: Type[T], to_load: ExternalType) -> T:
        marshaller = self.get_marshaller(type_)
        loaded = marshaller.load(to_load)
        return loaded

    def dump(self, obj: Any, type_: Optional[Type] = None) -> ExternalType:
        if not type_:
            type_ = type(obj)
        marshaller = self.get_marshaller(type_)
        dumped = marshaller.dump(obj)
        return dumped

    def get_marshaller(self, type_: Type[T]) -> MarshallerABC[T]:
        marshaller = self.marshallers_by_type.get(type_)
        if not marshaller:
            resolved_type = resolve_forward_refs(type_)
            for factory in self.factories:
                marshaller = factory.create(self, resolved_type)
                if marshaller:
                    break
            if not marshaller:
                raise MarshallError(f"no_marshaller_for_type:{type_}")
            self.marshallers_by_type[type_] = marshaller
        return marshaller

    def register_marshaller(self, marshaller: MarshallerABC):
        self.marshallers_by_type[marshaller.marshalled_type] = marshaller

    def register_factory(self, factory: MarshallerFactoryABC):
        self.factories.append(factory)
        self.factories.sort(key=lambda f: f.priority, reverse=True)


def create_marshy_context(injecty_context: Optional[InjectyContext] = None):
    if injecty_context is None:
        injecty_context = get_default_injecty_context()
    return MarshyContext(
        marshallers_by_type={
            m.marshalled_type: m for m in injecty_context.get_instances(MarshallerABC)
        },
        factories=injecty_context.get_instances(MarshallerFactoryABC),
        injecty_context=injecty_context,
    )
