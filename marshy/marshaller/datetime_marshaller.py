from datetime import datetime

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC


class DatetimeMarshaller(MarshallerABC[ExternalType]):
    """
    Marshaller for datetime instances to iso format
    """
    def __init__(self):
        super().__init__(datetime)

    def load(self, item: str) -> datetime:
        loaded = datetime.fromisoformat(item)
        return loaded

    def dump(self, item: datetime) -> str:
        dumped = item.isoformat()
        return dumped
