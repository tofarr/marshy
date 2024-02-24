from injecty import InjectyContext

from marshy.factory.dataclass_marshaller_factory import DataclassMarshallerFactory
from marshy.factory.enum_marshaller_factory import EnumMarshallerFactory
from marshy.factory.factory_marshaller_factory import FactoryMarshallerFactory
from marshy.factory.impl_marshaller_factory import ImplMarshallerFactory
from marshy.factory.list_marshaller_factory import ListMarshallerFactory
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.factory.optional_marshaller_factory import OptionalMarshallerFactory
from marshy.factory.tuple_marshaller_factory import TupleMarshallerFactory
from marshy.factory.union_marshaller_factory import UnionMarshallerFactory
from marshy.marshaller.as_str_marshaller import UuidMarshaller
from marshy.marshaller.bool_marshaller import BoolMarshaller
from marshy.marshaller.datetime_marshaller import DatetimeMarshaller
from marshy.marshaller.json_str_marshaller import (
    ExternalTypeMarshaller,
    ExternalItemTypeMarshaller,
    OptionalExternalItemTypeMarshaller,
)
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.marshaller.no_op_marshaller import NoneMarshaller
from marshy.marshaller.primitive_marshaller import (
    FloatMarshaller,
    IntMarshaller,
    StrMarshaller,
)

priority = 100


def configure(context: InjectyContext):
    context.register_impls(
        MarshallerABC,
        [
            FloatMarshaller,
            IntMarshaller,
            StrMarshaller,
            UuidMarshaller,
            NoneMarshaller,
            BoolMarshaller,
            DatetimeMarshaller,
            ExternalTypeMarshaller,
            ExternalItemTypeMarshaller,
            OptionalExternalItemTypeMarshaller,
        ],
    )
    context.register_impls(
        MarshallerFactoryABC,
        [
            EnumMarshallerFactory,
            UnionMarshallerFactory,
            OptionalMarshallerFactory,
            ListMarshallerFactory,
            FactoryMarshallerFactory,
            DataclassMarshallerFactory,
            TupleMarshallerFactory,
            ImplMarshallerFactory,
        ],
    )
