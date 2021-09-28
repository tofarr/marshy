from dataclasses import dataclass
from typing import Type, Optional

import typing_inspect

from marshy import marshaller_context
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller import marshaller_abc
from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller.iterable_marshaller import IterableMarshaller


@dataclass
class ListMarshallerFactory(MarshallerFactoryABC):
    priority: int = 100
    type_name_attr: str = '__type__'

    def create(self,
               context: marshaller_context.MarshallerContext,
               type_: Type) -> Optional[marshaller_abc.MarshallerABC]:
        origin = typing_inspect.get_origin(type_)
        if origin is list:
            item_type = typing_inspect.get_args(type_)[0]
            item_marshaller = DeferredMarshaller(item_type, context)
            marshaller = IterableMarshaller[item_type](type_, item_marshaller)
            return marshaller
