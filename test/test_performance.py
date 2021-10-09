from unittest import TestCase


class TestMarshallUuid(TestCase):
    """
    This just adds code coverage and makes sure the performance fixtures are working as expected
    Actual performance tests can be run from the command line like so:

    python -m timeit [-n N] [-r N] [-u U] [-s S] [-h] [statement ...]

python -m timeit -s "
from test.performance.marshmallow_performance import run
run(1000)
"

python -m timeit -s "
from test.performance.marshy_performance import run
run(1000)
"
    """

    def test_marshall(self):
        from test.performance import marshmallow_performance
        from test.performance import marshy_performance
        marshmallow_performance.run()
        marshy_performance.run()
        assert marshmallow_performance.product == marshy_performance.product
