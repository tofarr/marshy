from typing import TypeVar, Optional

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC

T = TypeVar('T')


class OptionalMarshaller(MarshallerABC[Optional[T]]):
    """
    Marshaller for optional types
    """

    def __init__(self, marshaller: MarshallerABC[T]):
        super().__init__(Optional[marshaller.marshalled_type])
        # noinspection PyDataclass
        self.marshaller = marshaller

    def load(self, item: ExternalType) -> Optional[T]:
        if item is not None:
            loaded = self.marshaller.load(item)
            return loaded

    def dump(self, item: Optional[T]) -> ExternalType:
        if item is not None:
            dumped = self.marshaller.dump(item)
            return dumped
