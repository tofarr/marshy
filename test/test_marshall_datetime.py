from datetime import datetime
from unittest import TestCase

from marshy import dump, load


class TestMarshallPrimitive(TestCase):

    def test_marshall(self):
        now = datetime.now().isoformat()
        loaded = load(datetime, now)
        dumped = dump(loaded)
        assert dumped == now

    def test_marshall_time(self):
        timestamp = '2021-01-01T12:34:56'
        loaded = load(datetime, timestamp)
        dumped = dump(loaded)
        assert dumped.startswith(timestamp)

    def test_marshall_tim_space(self):
        timestamp = '2021-01-01 12:34:56'
        loaded = load(datetime, timestamp)
        dumped = dump(loaded)
        assert dumped.startswith(timestamp.replace(' ', 'T'))
