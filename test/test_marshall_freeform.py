from unittest import TestCase

from marshy import dump, load
from marshy.types import ExternalItemType, ExternalType


class TestMarshallFreeform(TestCase):

    def test_marshall(self):
        values = dict(a=1, b=True, c=2.4, d='e', f=None)
        dumped = dump(values, ExternalType)
        expected = '{"a": 1, "b": true, "c": 2.4, "d": "e", "f": null}'
        assert expected == dumped
        loaded = load(ExternalItemType, dumped)
        assert values == loaded
