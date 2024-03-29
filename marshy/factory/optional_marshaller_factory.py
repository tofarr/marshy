from dataclasses import dataclass
from types import NoneType
from typing import Type, Optional, Union

import typing_inspect

from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller import marshaller_abc
from marshy.marshaller.optional_marshaller import OptionalMarshaller
from marshy.marshy_context import MarshyContext


@dataclass
class OptionalMarshallerFactory(MarshallerFactoryABC):
    priority: int = 100

    def create(
        self, context: MarshyContext, type_: Type
    ) -> Optional[marshaller_abc.MarshallerABC]:
        origin = typing_inspect.get_origin(type_)
        if origin == Union:
            optional_type = get_optional_type(type_)
            if optional_type:
                # noinspection PyTypeChecker
                return OptionalMarshaller[optional_type](
                    context.get_marshaller(optional_type)
                )


def get_optional_type(type_: Type) -> Optional[Type]:
    origin = typing_inspect.get_origin(type_)
    if origin == Union:
        args = typing_inspect.get_args(type_)
        if len(args) != 2:
            return None
        optional_args = [a for a in args if a != NoneType]
        if len(optional_args) == 1:
            return optional_args[0]
