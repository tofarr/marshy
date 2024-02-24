from dataclasses import dataclass
from typing import Optional, Type
from unittest import TestCase

from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.marshaller_context import MarshallerContext, marshy_context


class TestFactoryOrdering(TestCase):
    def test_factory_ordering_ascending(self):
        factories = [DummyFactory(i) for i in range(10)]
        sorted_factories = list(sorted(factories))
        assert sorted_factories == factories

    def test_factory_ordering_descending(self):
        factories = [DummyFactory(i) for i in range(10)]
        sorted_factories = list(sorted(factories, reverse=True))
        factories.reverse()
        assert sorted_factories == factories
        assert factories[0].create(marshy_context(), str) is None

    def test_factory_compare(self):
        a = DummyFactory(1)
        b = DummyFactory(2)
        assert a.__ne__(b)
        assert a.__eq__(a)

    def test_abc_methods(self):
        a = DummyFactory2()
        # noinspection PyTypeChecker
        assert a.create(None, None) is None
        assert a.priority == 0
        assert not a.__ne__(DummyFactory2())


@dataclass
class DummyFactory(MarshallerFactoryABC):
    priority: int = 0

    def create(
        self, context: MarshallerContext, type_: Type
    ) -> Optional[MarshallerABC]:
        return None


class DummyFactory2(MarshallerFactoryABC):
    def create(
        self, context: MarshallerContext, type_: Type
    ) -> Optional[MarshallerABC]:
        return None
