import inspect
from dataclasses import dataclass
from enum import Enum
from typing import Type, Optional

from marshy import marshaller_context
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller import marshaller_abc
from marshy.marshaller.enum_marshaller import EnumMarshaller


@dataclass
class EnumMarshallerFactory(MarshallerFactoryABC):
    priority: int = 100
    allow_unknown: bool = False

    def create(self,
               context: marshaller_context.MarshallerContext,
               type_: Type) -> Optional[marshaller_abc.MarshallerABC]:
        if inspect.isclass(type_) and issubclass(type_, Enum):
            return EnumMarshaller[type_](type_, self.allow_unknown)
