from typing import Type, Any, Optional, TypeVar

from marshy.marshy_context import marshy_context, MarshyContext
from marshy.types import ExternalType

_default_context = None
T = TypeVar("T")


# pylint: disable=W0603
def get_default_marshy_context() -> MarshyContext:
    global _default_context
    if not _default_context:
        _default_context = marshy_context()
    return _default_context


def load(type_: Type[T], to_load: ExternalType) -> T:
    return get_default_marshy_context().load(type_, to_load)


def dump(obj: Any, type_: Optional[Type] = None) -> ExternalType:
    return get_default_marshy_context().dump(obj, type_)
