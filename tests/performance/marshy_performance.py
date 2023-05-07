import marshy

from tests.performance.fixtures import Product, product


def run(iterations: int = 10):
    for i in range(iterations):
        dumped = marshy.dump(product)
        loaded = marshy.load(Product, dumped)
        assert loaded == product
