from typing import Optional, List
from unittest import TestCase

from marshy import dump, load


class TestMarshallIterable(TestCase):

    def test_marshall(self):
        values = [None, 'b']
        type_ = List[Optional[str]]
        dumped = dump(values, type_)
        assert values == dumped
        loaded = load(type_, dumped)
        assert values == loaded
