from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC


class BoolMarshaller(MarshallerABC[ExternalType]):

    def __init__(self):
        super().__init__(bool)

    def load(self, item: ExternalType) -> bool:
        if isinstance(item, str):
            return item.lower() not in ['', '0', '0.0', 'false']  # Custom falsy values
        return bool(item)

    def dump(self, item: bool) -> bool:
        return bool(item)
