from typing import Type, Optional, Dict

from marshy.marshaller.marshaller_abc import MarshallerABC


class TypeMarshaller(MarshallerABC[Type]):
    """
    Marshaller for object types - allows setting up a preset 'safe' list
    """
    _names_to_types: Dict[str, Type]
    _types_to_names: Dict[Type, str]

    def __init__(self):
        super().__init__(Type)
        object.__setattr__(self, '_names_to_types', {})
        object.__setattr__(self, '_types_to_names', {})

    def register(self, type_: Type, name: Optional[str] = None):
        if name is None:
            name = type_.__name__
        self._names_to_types[name] = type_
        self._types_to_names[type_] = name

    def load(self, item: str) -> Type:
        type_ = self._names_to_types[item]
        return type_

    def dump(self, item: Type) -> str:
        name = self._types_to_names[item]
        return name
