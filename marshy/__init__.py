import pkgutil
from typing import Type, Any, Optional, ForwardRef, TypeVar
import importlib

from marshy.types import ExternalType

_default_context = None
T = TypeVar('T')
CONFIG_MODULE_PREFIX = 'marshy_config_'


def get_default_context() -> ForwardRef('marshy.marshaller_context.MarshallerContext'):
    global _default_context
    if not _default_context:
        _default_context = new_default_context()
    return _default_context


def new_default_context() -> ForwardRef('marshy.marshaller_context.MarshallerContext'):
    from marshy.marshaller_context import MarshallerContext
    default_context = MarshallerContext()
    # Set up context based on naming convention
    module_info = (m for m in pkgutil.iter_modules() if m.name.startswith(CONFIG_MODULE_PREFIX))
    modules = [importlib.import_module(m.name) for m in module_info]
    modules.sort(key=lambda m: m.priority, reverse=True)
    for m in modules:
        getattr(m, 'configure')(default_context)
    return default_context


def load(type_: Type[T], to_load: ExternalType) -> T:
    return get_default_context().load(type_, to_load)


def dump(obj: Any, type_: Optional[Type] = None) -> ExternalType:
    return get_default_context().dump(obj, type_)
