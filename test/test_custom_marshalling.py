from typing import Optional, List, Iterable, Union, Sized
from unittest import TestCase

from marshy import ExternalType, new_default_context
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.marshaller_context import MarshallerContext


class TestCustomMarshalling(TestCase):
    """
    Higher level test of marshalling something completely custom. In this case we marshall a coordinate object as [x, y]
    and a dataset object as either a list of coordinates or a dictionary containing said list
    """
    def test_custom_marshall(self):
        to_load = [[n, n * n] for n in range(5)]
        loaded = context.load(Dataset, to_load)
        dumped = context.dump(loaded)
        assert dumped['median'] == [2, 8]
        assert dumped['mean'] == [2, 6]
        reloaded = context.load(Dataset, dumped)
        assert loaded == reloaded

    def test_fixtures(self):
        assert Coordinate(1, 2) != [1, 2]
        coords = set()
        coords.add(Coordinate(1, 2))
        coords.add(Coordinate(1, 2))
        assert len(coords) == 1
        assert str(Coordinate(1, 2)) == '[1, 2]'
        assert Dataset([]).calculate_mean() is None
        assert Dataset([]).calculate_median() is None
        assert Dataset([1, 2]) != Coordinate(1, 2)


class Coordinate:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return str([self.x, self.y])


class Dataset:
    def __init__(self, coordinates: Union[Iterable[Coordinate], Sized]):
        self.coordinates = coordinates

    def calculate_mean(self) -> Optional[Coordinate]:
        if not self.coordinates:
            return None
        return Coordinate(
            x=sum(c.x for c in self.coordinates) / len(self.coordinates),
            y=sum(c.y for c in self.coordinates) / len(self.coordinates)
        )

    def calculate_median(self) -> Optional[Coordinate]:
        if not self.coordinates:
            return None
        x = [c.x for c in self.coordinates]
        y = [c.y for c in self.coordinates]
        min_x = min(x)
        max_x = max(x)
        min_y = min(y)
        max_y = max(y)
        return Coordinate((min_x + max_x) / 2, (min_y + max_y) / 2)

    def __eq__(self, other):
        if isinstance(other, Dataset):
            return self.coordinates == other.coordinates
        return NotImplemented

    # noinspection PyUnusedLocal
    @classmethod
    def __marshaller_factory__(cls, marshaller_context: MarshallerContext):
        return DatasetMarshaller()


context = new_default_context()


class CoordinateMarshaller(MarshallerABC[Coordinate]):

    def __init__(self):
        super().__init__(Coordinate)

    def load(self, item: ExternalType) -> Coordinate:
        """ Accept coordinates in the format [x, y]"""
        return Coordinate(*item)

    def dump(self, item: Coordinate) -> ExternalType:
        """ Dump coordinates in the format [x, y] """
        return [item.x, item.y]


class DatasetMarshaller(MarshallerABC[Dataset]):

    def __init__(self):
        super().__init__(Dataset)

    def load(self, item: ExternalType) -> Dataset:
        """ Accept either a list of coordinates or a dict containing a list of coordinates """
        if isinstance(item, list):  # We accept a list of coordinates
            coordinates = item
        else:
            coordinates = item['coords']
        return Dataset(context.load(List[Coordinate], coordinates))

    def dump(self, item: Dataset) -> ExternalType:
        dumped = dict(coords=context.dump(item.coordinates, List[Coordinate]))
        if item.coordinates:
            dumped['mean'] = context.dump(item.calculate_mean(), Coordinate)
            dumped['median'] = context.dump(item.calculate_median(), Coordinate)
        return dumped


context.register_marshaller(CoordinateMarshaller())
