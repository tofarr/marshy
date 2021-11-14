from typing import Type
from unittest import TestCase

from marshy import new_default_context


class _UnknownType:
    pass


class TestMarshallIterable(TestCase):

    def test_marshall(self):
        context = new_default_context()
        assert context.dump(int, Type) == 'int'
        assert context.load(Type, 'int') == int

    def test_dump_unknown(self):
        context = new_default_context()
        with self.assertRaises(KeyError):
            context.dump(_UnknownType, Type)

    def test_load_unknown(self):
        context = new_default_context()
        with self.assertRaises(KeyError):
            context.load(Type, '_UnknownType')
