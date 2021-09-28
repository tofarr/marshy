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

## Circular References

Due to the fact that types in the object graph can self reference,
we defer resolution of most marshaller until as late as possible.
[DeferredMarshaller](marshy/marshaller/deferred_marshaller.py) 
is responsible for this, and means types can 
[self reference](test/test_marshall_deferred.py). 

Circular references within objects will still cause an error.
(Unless you decide on an error handling protocol for this an 
implement a custom Factory to deal with it!)

## Customizing the default context with an environment variable

Suppose you defined the following setup function int the directory
`/my_app/my_config.py` (Along with the `__init__.py`):

```
from marshy.default_context import new_default_context

def new_marshy_context():
    context = new_default_context()
    # context.register_marshaller( ... marshaller for some class that requires custom marshalling )
    # context.register_factory( ... some factory for custom logic - maybe circular reference resolution? )
    return context
```

On startup, if the environment variable is present, Marshy will
use this as the default rule configuration:
```
MARSHY_CONTEXT=my_app.my_config.new_marshy_context
```

## Building The Project

You need an account on pypi before this will work:

```
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install twine
python -m twine upload dist/*
```