from dataclasses import dataclass
from typing import List, Union
from unittest import TestCase

from marshy import dump, load
from marshy.marshy_context import create_marshy_context
from marshy.marshaller.union_marshaller import implementation_marshaller


class TestMarshallIterable(TestCase):
    def test_marshall(self):
        values = [True, None, 1, "Mix"]
        type_ = list[Union[bool, int, type(None), str]]
        dumped = dump(values, type_)
        assert dumped == [
            ["bool", True],
            ["NoneType", None],
            ["int", 1],
            ["str", "Mix"],
        ]
        loaded = load(type_, dumped)
        assert values == loaded

    def test_marshall_nested(self):
        type_ = Union[list[str], int]
        dumped = dump(["a", "b"], type_)
        assert dumped == ["list", ["a", "b"]]
        loaded = load(type_, dumped)
        assert loaded == ["a", "b"]
        dumped = dump(10, type_)
        assert dumped == ["int", 10]
        loaded = load(type_, dumped)
        assert loaded == 10

    def test_implementation_marshaller(self):
        class Base:
            pass

        @dataclass
        class VolcanoBase:
            magma_temperature: float = 2000.0

        @dataclass
        class MoonBase:
            has_laser: bool = False

        # I expect you to die!
        context = create_marshy_context()
        context.register_marshaller(
            implementation_marshaller(Base, (VolcanoBase, MoonBase), context)
        )
        moon_base = MoonBase(has_laser=True)
        # noinspection PyTestUnpassedFixture
        dumped = context.dump(moon_base, Base)
        assert dumped == ["MoonBase", dict(has_laser=True)]
        # noinspection PyTestUnpassedFixture
        loaded = context.load(Base, dumped)
        assert loaded == MoonBase(has_laser=True)

        volcano_base = VolcanoBase(magma_temperature=2100.0)
        # noinspection PyTestUnpassedFixture
        dumped = context.dump(volcano_base, Base)
        assert dumped == ["VolcanoBase", dict(magma_temperature=2100.0)]
        # noinspection PyTestUnpassedFixture
        loaded = context.load(Base, dumped)
        assert volcano_base == loaded
