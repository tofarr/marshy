from unittest import TestCase

from marshy import dump, load


class TestMarshallPrimitive(TestCase):

    def test_marshall(self):
        primitives = ['foobar', 10, 13.2]
        for p in primitives:
            dumped = dump(p)
            assert p == dumped
            loaded = load(p.__class__, dumped)
            assert p == loaded

    def test_marshall_str(self):
        primitives = ['foobar', 10, 13.2]
        for p in primitives:
            s = str(p)
            loaded = load(p.__class__, s)
            assert p == loaded
