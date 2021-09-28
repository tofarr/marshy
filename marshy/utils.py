import importlib
from typing import Type, List, Dict

import typing_inspect

from marshy.errors import MarshallError


def resolve_forward_refs(type_: Type) -> Type:
    origin = typing_inspect.get_origin(type_)
    if origin:
        args = list(resolve_forward_refs(a) for a in typing_inspect.get_args(type_))
        if origin is list:
            origin = List
        elif origin is dict:
            origin = Dict
        return origin[tuple(args)]
    if not typing_inspect.is_forward_ref(type_):
        return type_
    import_name = typing_inspect.get_forward_arg(type_)
    import_path = import_name.split('.')
    import_module = '.'.join(import_path[:-1])
    if not import_module:
        raise MarshallError(f'InvalidForwardRef:{type_}:Use full module name!')
    imported_module = importlib.import_module('.'.join(import_path[:-1]))
    return_type = getattr(imported_module, import_path[-1])
    return return_type
