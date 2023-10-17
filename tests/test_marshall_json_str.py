from typing import Optional
from unittest import TestCase

import marshy
from marshy import ExternalType
from marshy.types import ExternalItemType


class TestMarshallJsonStr(TestCase):

    def test_marshall_external_type(self):
        value = {"foo": [1, True, "bar"]}
        dumped = marshy.dump(value, ExternalType)
        self.assertEqual('{"foo": [1, true, "bar"]}', dumped)
        result = marshy.load(ExternalType, dumped)
        self.assertEqual(value, result)

    def test_marshall_external_item_type(self):
        value = {"foo": [1, True, "bar"]}
        dumped = marshy.dump(value, ExternalItemType)
        self.assertEqual('{"foo": [1, true, "bar"]}', dumped)
        result = marshy.load(ExternalItemType, dumped)
        self.assertEqual(value, result)

    def test_marshall_optional_external_item_type(self):
        value = {"foo": [1, True, "bar"]}
        dumped = marshy.dump(value, Optional[ExternalItemType])
        self.assertEqual('{"foo": [1, true, "bar"]}', dumped)
        result = marshy.load(Optional[ExternalItemType], dumped)
        self.assertEqual(value, result)
        dumped = marshy.dump(None, Optional[ExternalItemType])
        self.assertEqual("null", dumped)
        result = marshy.load(Optional[ExternalType], dumped)
        self.assertIsNone(result)
