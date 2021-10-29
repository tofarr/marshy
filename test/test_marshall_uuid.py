from unittest import TestCase
from uuid import uuid4, UUID

from marshy import dump, load


class TestMarshallUuid(TestCase):

    def test_marshall(self):
        for i in range(5):
            uuid = uuid4()
            dumped = dump(uuid)
            loaded = load(UUID, dumped)
            assert loaded == uuid
            assert dumped == str(uuid)
