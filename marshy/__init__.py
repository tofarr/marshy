from typing import Type, Any, Optional

from marshy.types import ExternalType

_default_context = None


def get_default_context():
    global _default_context
    if not _default_context:
        from marshy.default_context import new_default_context
        _default_context = new_default_context()
    return _default_context


def load(type_: Type, to_load: ExternalType):
    return get_default_context().load(type_, to_load)


def dump(obj: Any, type_: Optional[Type] = None) -> ExternalType:
    return get_default_context().dump(obj, type_)
