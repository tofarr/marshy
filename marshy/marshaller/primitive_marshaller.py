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
