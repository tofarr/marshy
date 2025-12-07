from typing import List, Union, Set
from unittest import TestCase

from marshy import dump, load
from marshy.errors import MarshallError


class TestMarshallIterable(TestCase):
    def test_marshall(self):
        values = list(range(10))
        dumped = dump(values, list[int])
        loaded = load(list[int], dumped)
        assert values == loaded

    def test_marshall_set(self):
        values = set(range(10))
        dumped = dump(values, Set[int])
        loaded = load(Set[int], dumped)
        assert values == loaded

    def test_dump(self):
        values = [True, None, 1, "Mix"]
        type_ = list[Union[bool, int, type(None), str]]
        dumped = dump(values, type_)
        loaded = load(type_, dumped)
        assert values == loaded

    def test_no_args(self):
        values = [True, None, 1, "Mix"]
        with self.assertRaises(MarshallError):
            dump(values)

    def test_load_no_args(self):
        values = [True, None, 1, "Mix"]
        with self.assertRaises(MarshallError):
            load(list, values)
