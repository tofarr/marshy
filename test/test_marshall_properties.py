from dataclasses import dataclass
from typing import Optional
from unittest import TestCase

from marshy import load, dump, get_default_context, new_default_context
from marshy.errors import MarshallError
from marshy.factory.dataclass_marshaller_factory import dataclass_marshaller, skip
from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller.property_marshaller import PropertyConfig


@dataclass
class President:
    name: str

    @property
    def initials(self) -> str:
        return ''.join(t[0].upper() for t in self.name.split(' '))

    @property
    def dob(self) -> Optional[str]:
        return getattr(self, 'lazy_value', None)

    @dob.setter
    def dob(self, lazy_value: Optional[str]):
        setattr(self, 'lazy_value', lazy_value)


@dataclass
class Unannotated:
    """
    This class is lacking an annotation - there is no way to
    automatically figure out a type for the 'typeless' property
    """
    @property
    def typeless(self):
        return getattr(self, '_foo', None)

    @typeless.setter
    def typeless(self, foo):
        setattr(self, '_foo', foo)


class TestMarshallProperties(TestCase):

    def test_property_marshalling(self):
        fdr = President('Franklin Delano Roosevelt')
        dumped = dump(fdr)
        assert dumped == dict(initials='FDR', name='Franklin Delano Roosevelt')
        loaded = load(President, dumped)
        assert loaded == fdr

    def test_property_marshalling_with_setter(self):
        jfk = dict(name='John Fitzgerald Kennedy', dob='May 29, 1917', initials='Ignored when loading')
        loaded = load(President, jfk)
        assert loaded == President(name='John Fitzgerald Kennedy')
        dumped = dump(loaded)
        jfk['initials'] = 'JFK'  # much better!
        assert dumped == jfk

    def test_unannotated_property(self):
        with self.assertRaises(MarshallError):
            get_default_context().get_marshaller(Unannotated)

    def test_unannotated_custom_property(self):
        context = new_default_context()
        marshaller = dataclass_marshaller(
            Unannotated,
            context,
            custom_property_configs=[
                PropertyConfig(
                    'typeless',
                    DeferredMarshaller(President, context),
                    getattr(Unannotated, 'typeless')
                )
            ]
        )
        context.register_marshaller(marshaller)
        unannotated = dict(typeless=dict(name='John Fitzgerald Kennedy'))
        loaded = context.load(Unannotated, unannotated)
        dumped = context.dump(loaded)
        unannotated['typeless']['initials'] = 'JFK'
        assert unannotated == dumped

    def test_skip(self):
        assert skip('a', [], [])
        assert not skip('a', None, None)
        assert not skip('a', ['a'], None)
        assert skip('a', None, ['a'])
        assert skip('a', [], ['b'])
        assert not skip('a', ['a'], ['b'])
        assert skip('a', ['a'], ['a'])
