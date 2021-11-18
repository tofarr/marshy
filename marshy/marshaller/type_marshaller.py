import importlib
from dataclasses import dataclass, field
from typing import Type, Iterable, Dict

from marshy.errors import MarshallError
from marshy.marshaller.marshaller_abc import MarshallerABC


@dataclass(frozen=True)
class TypeMarshaller(MarshallerABC[Type]):
    """
    Marshaller for object types - allows setting up a preset 'safe' module list
    """
    marshalled_type: Type = Type
    permitted_prefixes: Iterable[str] = field(default_factory=tuple)
    _names_to_types: Dict[str, Type] = field(default_factory=dict)
    _types_to_names: Dict[Type, str] = None

    def __post_init__(self):
        types_to_names = {t: n for n, t in self._names_to_types.items()}
        object.__setattr__(self, '_types_to_names', types_to_names)

    def load(self, item: str) -> Type:
        type_ = self._names_to_types.get(item)
        if type_ is not None:
            return type_
        for permitted_prefix in self.permitted_prefixes:
            if item.startswith(permitted_prefix):
                path = item.split('.')
                module = '.'.join(path[:-1])
                module = importlib.import_module(module)
                type_ = getattr(module, path[-1])
                self._names_to_types[item] = type_
                self._types_to_names[type_] = item
                return type_
        raise MarshallError(f'type_not_permitted:{item}')

    def dump(self, item: Type) -> str:
        name = self._types_to_names.get(item)
        if name is not None:
            return name
        path = item.__module__ + '.' + item.__name__
        for permitted_prefix in self.permitted_prefixes:
            if path.startswith(permitted_prefix):
                self._names_to_types[path] = item
                self._types_to_names[item] = path
                return path
        raise MarshallError(f'type_not_permitted:{item}')
