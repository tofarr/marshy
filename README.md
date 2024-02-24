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
# result == dict(title='Thingy', description=None, tags=['a','b'])
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
import marshy
from functools import reduce
import dataclasses

@dataclasses.dataclass
class Factorial:
  value: int
  
  @property
  def factorial(self) -> int:
    return reduce(lambda a, b: a*b, range(1, self.value+1))
    
factorial = Factorial(4)
dumped = marshy.dump(factorial)
# dumped == dict(value=4, factorial=24)
loaded = marshy.load(Factorial, dumped)
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
* A [MarshyContext](marshy/marshy_context.py): coordinates
  the activities of Marshallers and Factories

## Creating a Custom Marshaller Context

If you need multiple independent sets of rules for
marshalling data, then you should create your own marshalling
contexts and store references to them. The default works well
otherwise:

```
# Create a new blank marshy context - this will fail
# because there are no preset types or factories.
from marshy.marshy_context import MarshyContext
my_marshaller_context = MarshyContext()
dumped = my_marshaller_context.dump(Doohickey('Thingy'))

# Create a new marshaller context which copies the default rules.
from marshy.marshy_context import marshy_context
my_default_context = marshy_context()
dumped = my_default_context.dump(Doohickey('Thingy'))
```

## Creating a Custom Marshaller

To customize marshalling for a type, write a marshaller and then
register it with your context:
```
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalType


class MyDoohickeyMarshaller(MarshallerABC[Doohickey]):
    marshalled_type = Doohickey

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
from marshy import dump, get_default_marshy_context
from marshy.marshaller.bool_marshaller import BoolMarshaller
from marshy.marshaller.primitive_marshaller import StrMarshaller
from marshy.marshaller.obj_marshaller import attr_config, ObjMarshaller
attr_marshallers = [
    attr_config(StrMarshaller(), "title"),
    attr_config(BoolMarshaller(), "tags"),
]
get_default_marshy_context().register_marshaller(ObjMarshaller(Doohickey, attr_marshallers))
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
       
class PointMarshaller(MarshallerABC[Point]):
    marshalled_type = Point

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

We use [Injecty](https://github.com/tofarr/injecty) to manage dependency injection. Since any top level module
injecty_config_* is automatically loaded, our [injecty_config_marshy.py](injecty_config_marshy.py) defines our
default Marshaller / Factory implementations.

## Adding Polymorphic Implementations

We also use injecty to find polymorphic implementations of types to marshall / unmarshall. 
Taking the following classes where `Pet` has implementations `Cat` and `Dog`:

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
from injecty import get_default_injecty_context
import marshy
get_default_injecty_context().register_impls(PetAbc, [Cat, Dog])
pet = ['Cat', dict(name='Felix')]
loaded = marshy.load(PetAbc, pet)
```

[Tests for this are here](test/test_impl_marshaller.py)

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


## Release Procedure

![status](https://github.com/tofarr/marshy/actions/workflows/quality.yml/badge.svg?branch=main)

The typical process here is:
* Create a PR with changes. Merge these to main (The `Quality` workflows make sure that your PR
  meets the styling, linting, and code coverage standards).
* New releases created in github are automatically uploaded to pypi
