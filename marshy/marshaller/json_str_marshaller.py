import json
from typing import TypeVar, Type, Optional

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

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


class ExternalTypeMarshaller(JsonStrMarshaller):
    marshalled_type: Type[ExternalType] = ExternalType


class ExternalItemTypeMarshaller(JsonStrMarshaller):
    marshalled_type: Type[ExternalItemType] = ExternalItemType


class OptionalExternalItemTypeMarshaller(JsonStrMarshaller):
    marshalled_type: Type[Optional[ExternalItemType]] = Optional[ExternalItemType]
