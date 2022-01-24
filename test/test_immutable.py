from dataclasses import field, dataclass
from typing import Tuple
from unittest import TestCase
from uuid import uuid4, UUID

from marshy import dump, load


@dataclass(frozen=True)
class Immutable:
    title: str
    id: UUID = field(default_factory=uuid4)
    tags: Tuple[str, ...] = tuple()


MY_TUPLE = Tuple[bool, float, int, str]


class TestImmutable(TestCase):

    def test_marshall(self):
        immutable = Immutable('Test it!')
        dumped = dump(immutable)
        loaded = load(Immutable, dumped)
        assert loaded == immutable

    def test_marshall_non_empty(self):
        immutable = Immutable('Test it!', tags=('foo', 'bar', 'zap'))
        dumped = dump(immutable)
        loaded = load(Immutable, dumped)
        assert loaded == immutable

    def test_marshall_my_tuple(self):
        my_tuple: MY_TUPLE = (True, 1.2, 3, 'foo')
        dumped = dump(my_tuple, MY_TUPLE)
        loaded = load(MY_TUPLE, dumped)
        assert loaded == my_tuple
