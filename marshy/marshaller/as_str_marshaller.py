from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC


class AsStrMarshaller(MarshallerABC[ExternalType]):
    """
    Marshaller for cases where item is easily converted back and forth from strings
    """

    def load(self, item: ExternalType) -> ExternalType:
        return None if item is None else self.marshalled_type(item)

    def dump(self, item: ExternalType) -> ExternalType:
        return str(item)
