from enum import Enum
from unittest import TestCase

from marshy import dump, load, get_default_context
from marshy.errors import MarshallError
from marshy.factory.enum_marshaller_factory import EnumMarshallerFactory


class VehicleTypes(Enum):
    CAR = 'car'
    TRUCK = 'truck'
    BIKE = 'bike'


class TestMarshallEnum(TestCase):

    def test_marshall(self):
        dumped = dump(VehicleTypes.CAR)
        assert VehicleTypes.CAR.value == dumped
        loaded = load(VehicleTypes, dumped)
        assert VehicleTypes.CAR == loaded

    def test_unknown_value_not_permitted(self):
        with self.assertRaises(MarshallError):
            load(VehicleTypes, 'spaceship')

    def test_unknown_value_permitted(self):
        # Allow unknown values to be placed in the enum
        marshaller = EnumMarshallerFactory(allow_unknown=True).create(get_default_context(), VehicleTypes)
        loaded = marshaller.load('spaceship')
        assert loaded.value == 'spaceship'
        assert loaded.__class__ == VehicleTypes
        dumped = marshaller.dump(loaded)
        assert dumped == 'spaceship'
