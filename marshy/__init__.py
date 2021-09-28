import os
from typing import Type, Any, Optional
import importlib

from marshy.types import ExternalType

_default_context = None
MARSHY_CONTEXT = 'MARSHY_CONTEXT'


def get_default_context():
    global _default_context
    if not _default_context:
        # Set up the default_context based on an environment variable
        import_name = os.environ.get(MARSHY_CONTEXT, 'marshy.default_context.new_default_context')
        import_path = import_name.split('.')
        import_module = '.'.join(import_path[:-1])
        imported_module = importlib.import_module(import_module)
        marshy_context_fn = getattr(imported_module, import_path[-1])
        _default_context = marshy_context_fn()
    return _default_context


def load(type_: Type, to_load: ExternalType):
    return get_default_context().load(type_, to_load)


def dump(obj: Any, type_: Optional[Type] = None) -> ExternalType:
    return get_default_context().dump(obj, type_)
