from dataclasses import dataclass, field
from typing import Optional, List
from uuid import uuid4


def new_id() -> str:
    """ Required because marshmallow dataclass is difficult to customize """
    return str(uuid4())


@dataclass
class Tag:
    title: str
    id: str = field(default_factory=new_id)


@dataclass
class Product:
    title: str
    id: str = field(default_factory=new_id)
    weight_in_kg: Optional[float] = None
    number_in_stock: Optional[int] = None
    active: bool = False
    tags: List[Tag] = field(default_factory=list)


product = Product(title='Widget', weight_in_kg=0.034, number_in_stock=501, active=True, tags=[
    Tag('Small'),
    Tag('On Sale'),
    Tag('Contains Plastic')
])
