from uuid import UUID

from marshy.factory.dataclass_marshaller_factory import DataclassMarshallerFactory
from marshy.factory.enum_marshaller_factory import EnumMarshallerFactory
from marshy.factory.factory_marshaller_factory import FactoryMarshallerFactory
from marshy.factory.list_marshaller_factory import ListMarshallerFactory
from marshy.factory.optional_marshaller_factory import OptionalMarshallerFactory
from marshy.factory.union_marshaller_factory import UnionMarshallerFactory
from marshy.marshaller import PrimitiveMarshaller, none_marshaller, bool_marshaller, datetime_marshaller
from marshy.marshaller.as_str_marshaller import AsStrMarshaller
from marshy.marshaller.type_marshaller import TypeMarshaller
from marshy.marshaller_context import MarshallerContext

priority = 100


def configure(context: MarshallerContext):
    for t in [float, int, str]:
        context.register_marshaller(PrimitiveMarshaller(t))
    for t in [UUID]:
        context.register_marshaller(AsStrMarshaller(t))
    context.register_marshaller(none_marshaller)
    context.register_marshaller(bool_marshaller)
    context.register_marshaller(datetime_marshaller)
    context.register_factory(EnumMarshallerFactory())
    context.register_factory(UnionMarshallerFactory())
    context.register_factory(OptionalMarshallerFactory())
    context.register_factory(ListMarshallerFactory())
    context.register_factory(FactoryMarshallerFactory())
    context.register_factory(DataclassMarshallerFactory())
    context.register_marshaller(new_type_marshaller())


def new_type_marshaller():
    type_marshaller = TypeMarshaller(tuple('builtins.'))
    return type_marshaller
