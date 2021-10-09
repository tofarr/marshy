import marshmallow_dataclass
from test.performance.fixtures import Product, product


def run(iterations: int = 10):
    schema = marshmallow_dataclass.class_schema(Product)()
    for i in range(iterations):
        dumped = schema.dump(product)
        loaded = schema.load(dumped)
        assert loaded == product
