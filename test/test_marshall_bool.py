from unittest import TestCase

from marshy import dump, load


class TestMarshallPrimitive(TestCase):

    def test_marshall(self):
        primitives = [True, False]
        for p in primitives:
            dumped = dump(p)
            assert p == dumped
            loaded = load(p.__class__, dumped)
            assert p == loaded

    def test_marshall_truthy_str(self):
        truthy = ['True', 'true', '1', 'anything']
        for t in truthy:
            loaded = load(bool, t)
            assert loaded

    def test_marshall_falsy_str(self):
        truthy = ['False', 'false', 'FALSE', '0', '0.0', '']
        for t in truthy:
            loaded = load(bool, t)
            assert not loaded
