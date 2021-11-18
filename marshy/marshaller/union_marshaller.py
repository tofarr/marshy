from typing import TypeVar, Optional, Dict, Type, List, Iterable

from marshy import ExternalType
from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.marshaller_context import MarshallerContext

T = TypeVar('T')


class UnionMarshaller(MarshallerABC[T]):
    """
    Marshaller for polymorphic types
    """

    # noinspection PyDataclass
    def __init__(self, marshalled_type: T, marshallers_by_name: Dict[str, MarshallerABC[T]]):
        super().__init__(marshalled_type)
        self.marshallers_by_name = marshallers_by_name
        self.names_by_type = {resolve_type(m.marshalled_type): n for n, m in marshallers_by_name.items()}

    def load(self, item: List[ExternalType]) -> T:
        type_name = item[0]
        marshaller = self.marshallers_by_name[type_name]
        loaded = marshaller.load(item[1])
        return loaded

    def dump(self, item: Optional[T]) -> List[ExternalType]:
        type_name = self.names_by_type[item.__class__]
        marshaller = self.marshallers_by_name[type_name]
        dumped = marshaller.dump(item)
        return [type_name, dumped]


def resolve_type(type_: Type) -> Type:
    return resolve_type(type_.__origin__) if hasattr(type_, '__origin__') else type_


def implementation_marshaller(base_type: Type, impls: Iterable[Type], marshaller_context: MarshallerContext):
    return UnionMarshaller(base_type, {
        i.__name__: DeferredMarshaller[i](i, marshaller_context) for i in impls
    })
