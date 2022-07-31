from dataclasses import dataclass
from unittest import TestCase

from marshy import new_default_context
from marshy.factory.dataclass_marshaller_factory import DataclassMarshallerFactory


class TestCustomizeExcludeDumpedValues(TestCase):

    def test_remove_red(self):
        context = new_default_context()
        context.register_factory(DataclassMarshallerFactory(101, ('red',)))
        self.assertEqual(dict(), context.dump(Color()))
        self.assertEqual(dict(), context.dump(Color('red')))
        self.assertEqual(dict(name='blue'), context.dump(Color('blue')))


@dataclass
class Color:
    name: str = 'red'
