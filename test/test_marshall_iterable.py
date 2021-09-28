from typing import List, Union
from unittest import TestCase

from marshy import dump, load
from marshy.errors import MarshallError


class TestMarshallIterable(TestCase):

    def test_marshall(self):
        values = list(range(10))
        dumped = dump(values, List[int])
        loaded = load(List[int], dumped)
        assert values == loaded

    def test_dump(self):
        values = [True, None, 1, 'Mix']
        type_ = List[Union[bool, int, type(None), str]]
        dumped = dump(values, type_)
        loaded = load(type_, dumped)
        assert values == loaded

    def test_no_args(self):
        values = [True, None, 1, 'Mix']
        with self.assertRaises(MarshallError):
            dump(values)

    def test_load_no_args(self):
        values = [True, None, 1, 'Mix']
        with self.assertRaises(MarshallError):
            load(list, values)
