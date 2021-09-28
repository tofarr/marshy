from dataclasses import dataclass
from typing import Type, Optional, Union

import typing_inspect

from marshy import marshaller_context
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller import marshaller_abc
from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller.union_marshaller import UnionMarshaller


@dataclass
class UnionMarshallerFactory(MarshallerFactoryABC):
    priority: int = 90

    def create(self,
               context: marshaller_context.MarshallerContext,
               type_: Type) -> Optional[marshaller_abc.MarshallerABC]:
        origin = typing_inspect.get_origin(type_)
        if origin == Union:
            marshallers = {name_for_type(t): DeferredMarshaller(t, context) for t in typing_inspect.get_args(type_)}
            return UnionMarshaller[type_](type_, marshallers)


def name_for_type(type_: Type) -> str:
    if hasattr(type_, '__origin__'):
        return name_for_type(type_.__origin__)
    return type_.__name__ if hasattr(type_, '__name__') else str(type_)
