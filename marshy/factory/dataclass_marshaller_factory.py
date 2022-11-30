import dataclasses
import inspect
from typing import Type, Optional, List, get_type_hints, Tuple

from marshy import marshaller_context
from marshy.errors import MarshallError
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller import marshaller_abc
from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller.obj_marshaller import ObjMarshaller, AttrConfig, attr_config
from marshy.marshaller.property_marshaller import PropertyConfig, PropertyMarshaller
from marshy.marshaller_context import MarshallerContext
from marshy.utils import resolve_forward_refs


@dataclasses.dataclass
class DataclassMarshallerFactory(MarshallerFactoryABC):
    priority: int = 100
    exclude_dumped_values: Tuple = tuple()

    def create(self,
               context: marshaller_context.MarshallerContext,
               type_: Type) -> Optional[marshaller_abc.MarshallerABC]:
        if not dataclasses.is_dataclass(type_):
            return
        return dataclass_marshaller(type_, context, exclude_dumped_values=self.exclude_dumped_values)


def get_property_configs_for_type(type_: Type,
                                  context: MarshallerContext,
                                  include: Optional[List[str]] = None,
                                  exclude: Optional[List[str]] = None,
                                  exclude_dumped_values: Tuple = DataclassMarshallerFactory.exclude_dumped_values):
    property_configs = []
    for p in inspect.getmembers(type_, lambda o: isinstance(o, property)):
        name = p[0]
        if skip(name, include, exclude):
            continue
        prop = p[1]
        type_hints = get_type_hints(prop.fget)
        if 'return' not in type_hints:
            raise MarshallError(f'UnannotatedProperty:{type_}:{name}')
        prop_type = type_hints.get('return')

        prop_type = resolve_forward_refs(prop_type)
        marshaller = DeferredMarshaller[prop_type](prop_type, context)
        property_config = PropertyConfig(name, marshaller, prop, load=bool(prop.fset),
                                         exclude_dumped_values=exclude_dumped_values)
        property_configs.append(property_config)
    return property_configs


def skip(name: str, include: Optional[List[str]], exclude: Optional[List[str]]) -> bool:
    if include is not None and name not in include:
        return True
    if exclude is not None and name in exclude:
        return True
    return False


def get_attr_configs_for_type(type_: Type,
                              context: marshaller_context.MarshallerContext,
                              include: Optional[List[str]] = None,
                              exclude: Optional[List[str]] = None,
                              exclude_dumped_values: Tuple = (None,)):
    # noinspection PyDataclass
    fields: List[dataclasses.Field] = dataclasses.fields(type_)
    try:
        types = get_type_hints(type_, globalns=None, localns=None)
        attr_configs = [attr_config(internal_name=f.name, marshaller=DeferredMarshaller(types[f.name], context),
                                    exclude_dumped_values=exclude_dumped_values)
                        for f in fields if not skip(f.name, include, exclude)]
    except NameError:
        # Still supporting old style forward refs without futures...
        attr_configs = [attr_config(internal_name=f.name, marshaller=DeferredMarshaller(f.type, context),
                                    exclude_dumped_values=exclude_dumped_values)
                        for f in fields if not skip(f.name, include, exclude)]
    return attr_configs


def dataclass_marshaller(type_: Type,
                         context: marshaller_context.MarshallerContext,
                         custom_attr_configs: Optional[List[AttrConfig]] = None,
                         custom_property_configs: Optional[List[PropertyConfig]] = None,
                         include: Optional[List[str]] = None,
                         exclude: Optional[List[str]] = None,
                         exclude_dumped_values: Tuple = (None,)):
    exclude_list = exclude or []
    if custom_attr_configs:
        exclude_list.extend(a.external_name for a in custom_attr_configs)
    if custom_property_configs:
        exclude_list.extend(p.external_name for p in custom_property_configs)
    attr_configs = get_attr_configs_for_type(type_, context, include, exclude, exclude_dumped_values)
    property_configs = get_property_configs_for_type(type_, context, include, exclude_list, exclude_dumped_values)
    attr_configs.extend(custom_attr_configs or [])
    property_configs.extend(custom_property_configs or [])
    marshaller = ObjMarshaller[type_](type_, attr_configs)
    if property_configs:
        marshaller = PropertyMarshaller(marshaller, tuple(property_configs))
    return marshaller
