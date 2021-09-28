from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC


class NoOpMarshaller(MarshallerABC[ExternalType]):
    """
    Marshaller for NoOps (Mainly None)
    """
    def load(self, item: ExternalType) -> ExternalType:
        return item

    def dump(self, item: ExternalType) -> ExternalType:
        return item
