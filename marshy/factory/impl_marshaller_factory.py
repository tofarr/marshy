from dataclasses import dataclass, field
from typing import Type, Optional, Set

from marshy import marshaller_context, get_default_context
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.factory.union_marshaller_factory import name_for_type
from marshy.marshaller import marshaller_abc
from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller.union_marshaller import UnionMarshaller

MARSHALLER_FACTORY = '__marshaller_factory__'


@dataclass
class ImplMarshallerFactory(MarshallerFactoryABC):
    base: Type
    impls: Set[Type] = field(default_factory=set)
    priority: int = 110

    def create(self,
               context: marshaller_context.MarshallerContext,
               type_: Type) -> Optional[marshaller_abc.MarshallerABC]:
        if type_ is self.base:
            marshallers = {name_for_type(t): DeferredMarshaller[t](t, context) for t in self.impls}
            return UnionMarshaller[self.base](self.base, marshallers)

    def add_impl(self, impl):
        self.impls.add(impl)


def register_impl(base, impl, context: Optional[marshaller_context.MarshallerContext] = None):
    if context is None:
        context = get_default_context()
    for factory in context.get_factories():
        if isinstance(factory, ImplMarshallerFactory) and factory.base == base:
            factory.add_impl(impl)
            return
    factory = ImplMarshallerFactory(base)
    factory.add_impl(impl)
    context.register_factory(factory)
