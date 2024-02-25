from typing import Type, Any, Optional

from marshy.marshy_context import create_marshy_context, MarshyContext, T
from marshy.types import ExternalType

_default_context = None


# pylint: disable=W0603
def get_default_marshy_context() -> MarshyContext:
    global _default_context
    if not _default_context:
        _default_context = create_marshy_context()
    return _default_context


def load(type_: Type[T], to_load: ExternalType) -> T:
    return get_default_marshy_context().load(type_, to_load)


def dump(obj: Any, type_: Optional[Type] = None) -> ExternalType:
    return get_default_marshy_context().dump(obj, type_)
