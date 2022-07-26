from __future__ import annotations
from dataclasses import field, dataclass
from typing import Tuple, Optional, get_type_hints, List
from unittest import TestCase
from uuid import uuid4, UUID

from marshy import dump, load


@dataclass
class Nested:
    title: str
    children: List[Nested] = field(default_factory=list)


@dataclass
class FuturesAnnotated:
    title: str
    id: UUID = field(default_factory=uuid4)
    tags: Tuple[str, ...] = tuple()
    nested: Optional[Nested] = None

    @property
    def title_property(self) -> str:
        return self.title

    @title_property.setter
    def title_property(self, title_property: str):
        self.title = title_property


MY_TUPLE = Tuple[bool, Optional[Nested], int, str]

type_with_annotations = get_type_hints(FuturesAnnotated, globalns=None, localns=None)
print(type_with_annotations)


class TestFuturesAnnotated(TestCase):

    def test_marshall(self):
        immutable = FuturesAnnotated('Test it!')
        dumped = dump(immutable)
        loaded = load(FuturesAnnotated, dumped)
        assert loaded == immutable

    def test_marshall_non_empty(self):
        immutable = FuturesAnnotated('Test it!', tags=('foo', 'bar', 'zap'))
        dumped = dump(immutable)
        loaded = load(FuturesAnnotated, dumped)
        assert loaded == immutable

    def test_marshall_my_tuple(self):
        my_tuple: MY_TUPLE = (True, Nested('foo'), 3, 'foo')
        dumped = dump(my_tuple, MY_TUPLE)
        loaded = load(MY_TUPLE, dumped)
        assert loaded == my_tuple

    def test_marshall_my_tuple_optional(self):
        my_tuple: MY_TUPLE = (True, None, 3, 'foo')
        dumped = dump(my_tuple, MY_TUPLE)
        loaded = load(MY_TUPLE, dumped)
        assert loaded == my_tuple
