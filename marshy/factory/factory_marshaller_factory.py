from dataclasses import dataclass
from typing import Type, Optional

from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller import marshaller_abc
from marshy.marshy_context import MarshyContext

MARSHALLER_FACTORY = "__marshaller_factory__"


@dataclass
class FactoryMarshallerFactory(MarshallerFactoryABC):
    priority: int = 110

    def create(
        self, context: MarshyContext, type_: Type
    ) -> Optional[marshaller_abc.MarshallerABC]:
        factory = getattr(type_, MARSHALLER_FACTORY, None)
        if factory is not None:
            return factory(context)
