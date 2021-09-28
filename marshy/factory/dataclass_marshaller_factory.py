import dataclasses
from typing import Type, Optional, List

from marshy import marshaller_context
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller import marshaller_abc
from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller.obj_marshaller import ObjMarshaller


@dataclasses.dataclass
class DataclassMarshallerFactory(MarshallerFactoryABC):
    priority: int = 100
    filter_none = True  # Should values which are None be included in the output?

    def create(self,
               context: marshaller_context.MarshallerContext,
               type_: Type) -> Optional[marshaller_abc.MarshallerABC]:
        if dataclasses.is_dataclass(type_):
            # noinspection PyDataclass
            fields: List[dataclasses.Field] = dataclasses.fields(type_)
            attr_marshallers = {f.name: DeferredMarshaller(f.type, context) for f in fields}
            return ObjMarshaller[type_](type_, attr_marshallers, self.filter_none)
