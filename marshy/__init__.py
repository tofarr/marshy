from typing import Type, Any, Optional, ForwardRef, TypeVar

from marshy.marshaller_context import marshy_context
from marshy.types import ExternalType

_default_context = None
T = TypeVar("T")
CONFIG_MODULE_PREFIX = "marshy_config_"


# pylint: disable=W0603
def get_default_marshy_context() -> ForwardRef("marshy.marshaller_context.MarshallerContext"):
    global _default_context
    if not _default_context:
        _default_context = marshy_context()
    return _default_context


def load(type_: Type[T], to_load: ExternalType) -> T:
    return get_default_marshy_context().load(type_, to_load)


def dump(obj: Any, type_: Optional[Type] = None) -> ExternalType:
    return get_default_marshy_context().dump(obj, type_)
