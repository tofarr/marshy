from dataclasses import dataclass
from typing import Optional, List
from unittest import TestCase

from marshy import dump, load

# This is a little bit strange, but for python 3.7 forward references we have to include the full name or there will
# be no way to resolve it later
NodeTypeName = f'{__name__}.Node'


@dataclass
class Node:
    id: str
    # The fact that Node references itself means we need deferred resolution of the marshaller
    # Since it will also reference itself
    children: Optional[List[NodeTypeName]] = None


class TestMarshallDeferred(TestCase):

    def test_marshall(self):
        root = Node('root', [Node('child-a'), Node('child-b')])
        dumped = dump(root)
        loaded = load(Node, dumped)
        assert root == loaded
