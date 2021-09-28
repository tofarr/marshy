from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Union

from marshy.errors import MarshallError
from marshy.marshaller.marshaller_abc import MarshallerABC

T = TypeVar('T', bound=Enum)
ERROR_PREFIX = 'INVALID_VALUE__'


@dataclass(frozen=True)
class EnumMarshaller(MarshallerABC[T]):
    """
    Marshaller for enums
    """
    allow_unknown: bool = False

    def load(self, item: Union[str, int, float]) -> T:
        try:
            loaded = self.marshalled_type(item)
            return loaded
        except ValueError as e:
            if self.allow_unknown:
                pseudo_member = generate_pseudo_member(self.marshalled_type, item)
                return pseudo_member
            raise MarshallError(e)

    def dump(self, item: T) -> Union[str, int, float]:
        dumped = item.value
        return dumped


def generate_pseudo_member(enum: T, value: Union[str, int, float]):
    pseudo_member = object.__new__(enum)
    pseudo_member._name_ = f'{ERROR_PREFIX}{str(value).upper()}'
    pseudo_member._value_ = value
    # noinspection PyProtectedMember
    pseudo_member = enum._value2member_map_.setdefault(value, pseudo_member)
    return pseudo_member
