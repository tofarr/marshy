import json
from typing import TypeVar

from marshy.marshaller.marshaller_abc import MarshallerABC

T = TypeVar("T")


class JsonStrMarshaller(MarshallerABC[T]):
    """
    Marshaller for freeform json objects - they are interpreted as strings. (Due to technologies like graphql
    having a dislike for unstructured data)
    """

    def load(self, item: str) -> T:
        loaded = json.loads(item)
        return loaded

    def dump(self, item: T) -> str:
        dumped = json.dumps(item)
        return dumped
