from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import List
from unittest import TestCase

from marshy import dump, load, new_default_context
from marshy.factory.impl_marshaller_factory import register_impl


@dataclass
class PetAbc(ABC):
    name: str

    @abstractmethod
    def vocalize(self) -> str:
        """ What sound does this make? """


class Cat(PetAbc):

    def vocalize(self):
        return "Meow!"


class Dog(PetAbc):

    def vocalize(self) -> str:
        return "Woof!"


class TestImplMarshaller(TestCase):

    def test_marshall(self):
        context = new_default_context()
        register_impl(PetAbc, Cat, context)
        register_impl(PetAbc, Dog, context)
        pet = Cat('Felix')
        dumped = context.dump(pet, PetAbc)
        assert dumped == ['Cat', dict(name='Felix')]
        loaded = context.load(PetAbc, dumped)
        assert pet == loaded
        assert loaded.vocalize() == 'Meow!'

    def test_marshall_nested(self):
        register_impl(PetAbc, Cat)
        register_impl(PetAbc, Dog)
        pets = [Cat('Felix'), Dog('Rover')]
        dumped = dump(pets, List[PetAbc])
        assert dumped == [['Cat', dict(name='Felix')], ['Dog', dict(name='Rover')]]
        loaded = load(List[PetAbc], dumped)
        assert pets == loaded
        vocalizations = [p.vocalize() for p in loaded]
        assert ['Meow!', 'Woof!'] == vocalizations
