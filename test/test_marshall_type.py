from unittest import TestCase

from marshy.errors import MarshallError
from marshy.marshaller.type_marshaller import TypeMarshaller
from test.test_marshall_properties import President


class PermittedType:
    pass


class TestMarshallType(TestCase):

    def test_marshall(self):
        marshaller = TypeMarshaller(permitted_prefixes=(__name__,), _names_to_types=dict(int=int, str=str))
        assert marshaller.dump(int) == 'int'
        assert marshaller.load('int') == int

    def test_load_by_prefix(self):
        marshaller = TypeMarshaller(permitted_prefixes=(__name__,))
        assert marshaller.load(f'{__name__}.PermittedType') == PermittedType

    def test_dump_by_prefix(self):
        marshaller = TypeMarshaller(permitted_prefixes=(__name__,))
        assert marshaller.dump(PermittedType) == f'{__name__}.PermittedType'

    def test_dump_unknown(self):
        marshaller = TypeMarshaller(permitted_prefixes=(__name__,))
        with self.assertRaises(MarshallError):
            marshaller.dump(President)

    def test_load_unknown(self):
        marshaller = TypeMarshaller(permitted_prefixes=(__name__,))
        with self.assertRaises(MarshallError):
            marshaller.load('some.Unknown')
