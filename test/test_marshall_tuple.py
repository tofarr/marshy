from typing import Tuple
from unittest import TestCase

from marshy import dump, load


class TestMarshallTuple(TestCase):

    def test_marshall(self):
        type_ = Tuple[int, str, bool]
        values = (1, 'Foo', True)
        dumped = dump(values, type_)
        self.assertEqual([1, 'Foo', True], dumped)
        loaded = load(type_, dumped)
        self.assertEqual(values, loaded)

    def test_marshall_dict(self):
        type_ = Tuple[int, str, bool]
        values = dict(t0=1, t1='Foo', t2=True)
        loaded = load(type_, values)
        expected = (1, 'Foo', True)
        self.assertEqual(expected, loaded)
