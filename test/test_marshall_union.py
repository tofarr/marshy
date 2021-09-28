from typing import List, Union
from unittest import TestCase

from marshy import dump, load


class TestMarshallIterable(TestCase):

    def test_marshall(self):
        values = [True, None, 1, 'Mix']
        type_ = List[Union[bool, int, type(None), str]]
        dumped = dump(values, type_)
        assert dumped == [['bool', True], ['NoneType', None], ['int', 1], ['str', 'Mix']]
        loaded = load(type_, dumped)
        assert values == loaded

    def test_marshall_nested(self):
        type_ = Union[List[str], int]
        dumped = dump(['a', 'b'], type_)
        assert dumped == ['list', ['a', 'b']]
        loaded = load(type_, dumped)
        assert loaded == ['a', 'b']
        dumped = dump(10, type_)
        assert dumped == ['int', 10]
        loaded = load(type_, dumped)
        assert loaded == 10

