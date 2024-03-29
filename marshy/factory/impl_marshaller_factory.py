from dataclasses import dataclass
from typing import Type, Optional

from marshy.marshy_context import MarshyContext
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.factory.union_marshaller_factory import name_for_type
from marshy.marshaller import marshaller_abc
from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller.union_marshaller import UnionMarshaller

MARSHALLER_FACTORY = "__marshaller_factory__"


@dataclass(frozen=True)
class ImplMarshallerFactory(MarshallerFactoryABC):
    priority: int = 110

    def create(
        self, context: MarshyContext, type_: Type
    ) -> Optional[marshaller_abc.MarshallerABC]:
        # noinspection PyTypeChecker
        impls = context.injecty_context.get_impls(base=type_, permit_no_impl=True)
        if impls:
            marshallers = {
                name_for_type(i): DeferredMarshaller[i](i, context) for i in impls
            }
            return UnionMarshaller[type_](type_, marshallers)
