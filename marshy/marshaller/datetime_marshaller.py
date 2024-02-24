from datetime import datetime
from typing import Type

from marshy.marshaller.marshaller_abc import MarshallerABC


class DatetimeMarshaller(MarshallerABC[datetime]):
    """
    Marshaller for datetime instances to iso format
    """

    marshalled_type: Type[datetime] = datetime

    def load(self, item: str) -> datetime:
        loaded = datetime.fromisoformat(item)
        return loaded

    def dump(self, item: datetime) -> str:
        dumped = item.isoformat()
        return dumped
