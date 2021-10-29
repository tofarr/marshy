import importlib
import typing

import typing_inspect

from marshy.errors import MarshallError

_TYPES_BY_ORIGIN = {t.__origin__: t for t in typing.__dict__.values() if hasattr(t, '__origin__')}


def resolve_forward_refs(type_: typing.Type) -> typing.Type:
    origin = typing_inspect.get_origin(type_)
    if origin is not None:
        args = list(resolve_forward_refs(a) for a in typing_inspect.get_args(type_))
        typing_origin = _TYPES_BY_ORIGIN.get(origin)
        origin = typing_origin or origin
        return origin[tuple(args)]
    if not typing_inspect.is_forward_ref(type_):
        return type_
    import_name = typing_inspect.get_forward_arg(type_)
    import_path = import_name.split('.')
    import_module = '.'.join(import_path[:-1])
    if not import_module:
        raise MarshallError(f'InvalidForwardRef:{type_}:Use full module name!')
    imported_module = importlib.import_module(import_module)
    return_type = getattr(imported_module, import_path[-1])
    return return_type
