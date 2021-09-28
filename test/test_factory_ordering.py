from dataclasses import dataclass
from typing import Optional, Type
from unittest import TestCase

from marshy import get_default_context
from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.marshaller_context import MarshallerContext


class TestFactoryOrdering(TestCase):

    def test_factory_ordering_ascending(self):
        marshallers = [DummyFactory(i) for i in range(10)]
        sorted_marshallers = list(sorted(marshallers))
        assert sorted_marshallers == marshallers

    def test_factory_ordering_descending(self):
        marshallers = [DummyFactory(i) for i in range(10)]
        sorted_marshallers = list(sorted(marshallers, reverse=True))
        marshallers.reverse()
        assert sorted_marshallers == marshallers
        assert marshallers[0].create(get_default_context(), str) is None

    def test_factory_compare(self):
        a = DummyFactory(1)
        b = DummyFactory(2)
        assert a.__ne__(b)
        assert a.__eq__(a)


@dataclass
class DummyFactory(MarshallerFactoryABC):

    def create(self,
               context: MarshallerContext,
               type_: Type
               ) -> Optional[MarshallerABC]:
        return None
