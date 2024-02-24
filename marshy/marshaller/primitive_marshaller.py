from typing import Type

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC


class PrimitiveMarshaller(MarshallerABC[ExternalType]):
    """
    Marshaller for cases where the item is already an external type (int, float, str)
    """

    def load(self, item: ExternalType) -> ExternalType:
        return None if item is None else self.marshalled_type(item)

    def dump(self, item: ExternalType) -> ExternalType:
        return item


class FloatMarshaller(PrimitiveMarshaller):
    marshalled_type: Type[float] = float


class IntMarshaller(PrimitiveMarshaller):
    marshalled_type: Type[int] = int


class StrMarshaller(PrimitiveMarshaller):
    marshalled_type: Type[str] = str
