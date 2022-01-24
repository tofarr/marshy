from dataclasses import dataclass
from typing import Type, Optional

import typing_inspect

from marshy import marshaller_context
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller import marshaller_abc
from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller.iterable_marshaller import IterableMarshaller
from marshy.marshaller.tuple_marshaller import TupleMarshaller


@dataclass
class TupleMarshallerFactory(MarshallerFactoryABC):
    priority: int = 90
    type_name_attr: str = '__type__'

    def create(self,
               context: marshaller_context.MarshallerContext,
               type_: Type) -> Optional[marshaller_abc.MarshallerABC]:
        origin = typing_inspect.get_origin(type_)
        if origin is tuple:
            args = typing_inspect.get_args(type_)
            if len(args) == 2 and args[1] is Ellipsis:
                item_marshaller = DeferredMarshaller(args[0], context)
                marshaller = IterableMarshaller[type_](type_, item_marshaller, tuple)
                return marshaller
            marshallers = tuple(DeferredMarshaller(t, context) for t in args)
            return TupleMarshaller[type_](type_, marshallers)
