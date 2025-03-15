from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import List  # noqa
from unittest import TestCase

from injecty import create_injecty_context

from marshy.factory.impl_marshaller_factory import ImplMarshallerFactory
from marshy.marshy_context import create_marshy_context


@dataclass
class PetAbc(ABC):
    name: str

    @abstractmethod
    def vocalize(self) -> str:
        """What sound does this make?"""


class Cat(PetAbc):
    def vocalize(self):
        return "Meow!"


class Dog(PetAbc):
    def vocalize(self) -> str:
        return "Woof!"


class TestImplMarshaller(TestCase):
    def test_marshall(self):
        injecty_context = create_injecty_context()
        injecty_context.register_impls(PetAbc, [Cat, Dog])
        context = create_marshy_context(injecty_context=injecty_context)
        pet = Cat("Felix")
        dumped = context.dump(pet, PetAbc)
        assert dumped == ["Cat", dict(name="Felix")]
        loaded = context.load(PetAbc, dumped)
        assert pet == loaded
        assert loaded.vocalize() == "Meow!"

    def test_marshall_nested(self):
        injecty_context = create_injecty_context()
        injecty_context.register_impls(PetAbc, [Cat, Dog])
        context = create_marshy_context(injecty_context=injecty_context)
        pets = [Cat("Felix"), Dog("Rover")]
        dumped = context.dump(pets, list[PetAbc])
        assert dumped == [["Cat", dict(name="Felix")], ["Dog", dict(name="Rover")]]
        loaded = context.load(list[PetAbc], dumped)
        assert pets == loaded
        vocalizations = [p.vocalize() for p in loaded]
        assert ["Meow!", "Woof!"] == vocalizations
