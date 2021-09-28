from typing import Union, Optional, Dict
from unittest import TestCase

from marshy import __version__
from marshy.errors import MarshallError
from marshy.utils import resolve_forward_refs
import test


class TestResolveForwardRefs(TestCase):

    def test_one_hundred_percent(self):
        # Mostly because I want 100% test coverage
        assert __version__ is not None
        assert test is not None

    def test_type_hints(self):
        array = [int, str, bool, float, list, dict]
        for i in range(1, len(array)):
            permitted_types = array[0:i]
            type_ = Union[tuple(permitted_types)]
            resolve_forward_refs(type_)

    def test_invalid_import_module(self):
        with self.assertRaises(MarshallError):
            resolve_forward_refs(Optional['NotARealClassName'])

    def test_dict(self):
        type_ = Dict[str, 'unittest.TestCase']
        type_ = resolve_forward_refs(type_)
        assert type_ == Dict[str, TestCase]
