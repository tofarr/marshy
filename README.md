# Marshy - Better Marshalling for Python.

This project is a general purpose externalizer for python objects.
(Like Marshmallow or Pedantic) The guiding philosophy is convention
over configuration, with the aim of still making customizations as
pain free as possible, based on python type hints.

Out of the box, it supports primitives, dataclasses, and enums.

## Installation

`pip install marshy`

## General Usage

Given the following dataclass:
```
from typing import List, Optional
import dataclasses


@dataclasses.dataclass
class Doohickey:
  title: str
  description: Optional[str] = None
  tags: List[str] = dataclasses.field(default_factory=list)
```

Marshall data with:
```
import marshy
result = marshy.dump(Doohickey('Thingy', tags=['a','b']))
# result == dict(title='Thingy', tags=['a','b'])
```

Unmarshall data with:
```
result = marshy.load(Doohickey, dict(title='Thingy'))
# result == Doohickey('Thingy', description=None, tags=[])
```

## Custom properties

Custom properties are also serialized by default. (If they
have a setter, it is used when loading):

```
@dataclass
class Factorial:
  value: int
  
  @property
  def factorial(self) -> int:
    return reduce(lambda a, b: a*b, range(1, self.value+1))
    
factorial = Factorial(4)
dumped = dump(factorial)
# dumped == dict(value=4, factorial=24)
loaded = load(Factorial, dumped)
# loaded == factorial
```

## Under The Hood

Internally, API defines 3 core concepts:

* A [Marshaller](marshy/marshaller/marshaller_abc.py): Is 
  responsible for marshalling / unmarshalling a single type of
  object.
* A [MarshallerFactory](marshy/factory/marshaller_factory_abc.py): has
  a `create` method used to create marshallers for types, and has
  a priority which controls the order in which they are run. 
  (higher first)
* A [MarshallerContext](marshy/marshaller_context.py): coordinates
  the activities of Marshallers and Factories

## Creating a Custom Marshaller Context

If you need multiple independent sets of rules for
marshalling data, then you should create your own marshalling
contexts and store references to them. The default works well
otherwise:

```
# Dump a Doohickey using the default context (Same as marshy.dump...)
from marshy import get_default_context
dumped = get_default_context().dump(Doohickey('Thingy'))

# Create a new blank marshaller context - this will fail
# because there are no preset types or factories.
from marshy.marshaller_context import MarshallerContext
my_marshaller_context = MarshallerContext()
dumped = my_marshaller_context.dump(Doohickey('Thingy'))

# Create a new marshaller context which copies the default rules.
from marshy.default_context import new_default_context
my_default_context = new_default_context()
dumped = my_default_context.dump(Doohickey('Thingy'))
```

## Creating a Custom Marshaller

To customize marshalling for a type, write a marshaller and then
register it with your context:
```
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalType


class MyDoohickeyMarshaller(MarshallerABC[Doohickey]):

    def __init__(self):
        super().__init__(Doohickey)

    def load(self, item: ExternalType) -> Doohickey:
        return Doohickey(item[0], item[1], item[2])

    def dump(self, item: Doohickey) -> ExternalType:
        return [item.title, item.description, item.tags]

my_default_context.register_marshaller(MyDoohickeyMarshaller())
dumped = my_default_context.dump(Doohickey('Thingy'))
# dumped == ['Thingy', None, []]

loaded = my_default_context.load(Doohickey, dumped)
# dumped == Doohickey('Thingy')
```

## Creating a Custom Marshaller Factory

Sometimes you need to create a marshaller for a while concept of
object rather than a single type - In this case you need a factory,
(this is how the default rules work!). Examples:
* [ListMarshallerFactory](marshy/factory/list_marshaller_factory.py)
  looks for typed lists (e.g.,: List[str]) and creates marshallers
  for them - you already saw the results in `Doohickey.tags` above.
* [OptionalMarshallerFactory](marshy/factory/optional_marshaller_factory.py)
  looks for optional fields (e.g.,: Optional[str]) and creates 
  marshallers that mean each individual other marshaller does not
  need to accommodate the case where a value is None - just mark
  it optional!
* [DataClassMarshallerFactory](marshy/factory/dataclass_marshaller_factory.py)
  provides a marshaller for dataclasses assuming they have a standard
  constructor based on their fields.
  
## Customizing dataclass attributes:

Taking the doohickey example:

```
from marshy import dump, get_default_context
from marshy.marshaller import str_marshaller, bool_marshaller
from marshy.marshaller.obj_marshaller import ObjMarshaller
attr_marshallers = dict(title=str_marshaller, tags=bool_marshaller)
get_default_context().register_marshaller(ObjMarshaller(Doohickey, attr_marshallers, False))
dumped = dump(Doohickey('Thingy'))
# dumped == dict(title='Thingy', tags=False)
```

## Customizing dataclass marshalling

As an alternative to defining a custom marshaller / factory, it is possible to simply
define a __marshaller_factory__ class method. (Note: this becomes the default for all
contexts) Imagine a case where you have a dataclass representing a 2D point, which you
want to be marshalled in the format [x, y] (An array rather than the standard object):
```
from dataclasses import dataclass
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy import load, dump

@dataclass
class Point:
    x: float
    y: float
    
    @classmethod
    def __marshaller_factory__(cls, marshaller_context):
       return PointMarshaller()
       
class PointMarshaller(MarshallerABC):

    def __init__(self):
        super().__init__(Point)

    def load(self, item):
        return Point(item[0], item[1])
    
    def dump(self, item):
        return [item.x, item.y]
        
dumped = dump(Point(1.2, 3.4))
loaded = load(Point, dumped)
```

## Circular References

Due to the fact that types in the object graph can self reference,
we defer resolution of most marshaller until as late as possible.
[DeferredMarshaller](marshy/marshaller/deferred_marshaller.py) 
is responsible for this, and means types can 
[self reference](test/test_marshall_deferred.py). 

Circular references within objects will still cause an error.
(Unless you decide on an error handling protocol for this an 
implement a custom Factory to deal with it!)

## Customizing the default context

The project uses the namespace convention `marshy_config_` to identity configuration packages.
(https://packaging.python.org/guides/creating-and-discovering-plugins/). Configuration packages should have an integer
priority attribute, and a  `def configure(context: MarshallerContext)` function. e.g.:
[default_config](marshy_config_default/__init__.py)

## Adding Polymorphic Implementations

Taking the following polymorphic classes where `Pet` has implementations `Cat` and `Dog`:

```
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class PetAbc(ABC):
    name: str

    @abstractmethod
    def vocalize(self) -> str:
        """ What sound does this make? """


class Cat(PetAbc):

    def vocalize(self):
        return "Meow!"


class Dog(PetAbc):

    def vocalize(self) -> str:
        return "Woof!"
```

In order to deserialize a Pet, marshy needs to be informed tha the implementations exist. This can be done at any point 
in the configuration:

```
from marshy import load
from marshy.factory.impl_marshaller_factory import register_impl
register_impl(PetAbc, Cat)
register_impl(PetAbc, Dog)
pet = ['Cat', dict(name='Felix')]
loaded = load(PetAbc, pet)
```

[Tests for this are here] (test/test_impl_marshaller.py)

## Performance Tests

Basic Tests show performance is approximate with marshmallow:

```
python -m timeit -s "
from test.performance.marshy_performance import run
run(1000)
"
```

```
python -m timeit -s "
from test.performance.marshmallow_performance import run
run(1000)
"
```


## Building The Project

You need an account on pypi before this will work:

```
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install twine
python -m twine upload dist/*
```