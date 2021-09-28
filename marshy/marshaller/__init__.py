from marshy.marshaller.NoOpMarshaller import NoOpMarshaller
from marshy.marshaller.bool_marshaller import BoolMarshaller
from marshy.marshaller.primitive_marshaller import PrimitiveMarshaller


bool_marshaller = BoolMarshaller()
float_marshaller = PrimitiveMarshaller(float)
int_marshaller = PrimitiveMarshaller(int)
str_marshaller = PrimitiveMarshaller(str)

none_marshaller = NoOpMarshaller(type(None))
