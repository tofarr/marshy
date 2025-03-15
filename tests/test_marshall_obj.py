from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from unittest import TestCase

from marshy import dump, load
from marshy.factory.dataclass_marshaller_factory import dataclass_marshaller
from marshy.marshaller.bool_marshaller import BoolMarshaller
from marshy.marshaller.obj_marshaller import ObjMarshaller, attr_config
from marshy.marshaller.optional_marshaller import OptionalMarshaller
from marshy.marshaller.primitive_marshaller import (
    StrMarshaller,
    IntMarshaller,
    FloatMarshaller,
)
from marshy.marshy_context import create_marshy_context

# This is a little bit strange, but for these forward references we have to include the full name or there will be no
# way to resolve it later
PurchaseTypeName = f"{__name__}.Purchase"


@dataclass
class Customer:
    id: str
    full_name: str
    address: Optional[str] = None
    purchases: Optional[list[PurchaseTypeName]] = None


@dataclass
class Product:
    id: str
    title: str
    description: Optional[str] = None
    weight_in_kg: Optional[float] = None
    purchases: Optional[list[PurchaseTypeName]] = None


@dataclass
class Purchase:
    id: str
    date: str
    customer: Optional[Customer] = None
    product: Optional[Product] = None


class TestMarshallObj(TestCase):
    def test_marshall(self):
        marshaller = ObjMarshaller(
            dict,
            (
                attr_config(IntMarshaller(), "i"),
                attr_config(StrMarshaller(), "s"),
                attr_config(FloatMarshaller(), "f"),
                attr_config(BoolMarshaller(), "b"),
                attr_config(
                    OptionalMarshaller(IntMarshaller()),
                    "n",
                    exclude_dumped_values=(None,),
                ),
            ),
        )
        value: dict[str, Any] = dict(i=10, s="foo", f=12.2, b=True, n=None)
        dumped = marshaller.dump(value)
        assert "n" not in dumped
        loaded = marshaller.load(dumped)
        del value["n"]
        assert loaded == value

    def test_marshall_no_filter_none(self):
        marshaller = ObjMarshaller(
            dict,
            (
                attr_config(IntMarshaller(), "i"),
                attr_config(StrMarshaller(), "s"),
                attr_config(FloatMarshaller(), "f"),
                attr_config(BoolMarshaller(), "b"),
                attr_config(OptionalMarshaller(IntMarshaller()), "n"),
            ),
        )
        value: dict[str, Any] = dict(i=10, s="foo", f=12.2, b=True, n=None)
        dumped = marshaller.dump(value)
        assert "n" in dumped
        loaded = marshaller.load(dumped)
        assert loaded == value

    def test_marshall_single_entity(self):
        customer = Customer("buyer-1", "Buyer 1")
        dumped = dump(customer)
        loaded = load(Customer, dumped)
        assert customer == loaded

    def test_marshall_nested_entities(self):
        customer = Customer(
            "buyer-1",
            "Buyer 1",
            purchases=[
                Purchase(
                    "purchase-1",
                    "2000-01-01",
                    product=Product("product-1", "Product 1", weight_in_kg=10.2),
                ),
                Purchase(
                    "purchase-2",
                    "2000-01-01",
                    product=Product("product-2", "Product 2", weight_in_kg=5.3),
                ),
                Purchase(
                    "purchase-3",
                    "2000-01-02",
                    product=Product("product-1", "Product 1", weight_in_kg=10.2),
                ),
            ],
        )
        dumped = dump(customer)
        loaded = load(Customer, dumped)
        assert customer == loaded

    def test_marshall_custom_attr(self):
        """
        Test Marshaller which capitalizes the attribute name for ID
        """
        context = create_marshy_context()
        context.register_marshaller(
            dataclass_marshaller(
                Customer,
                context,
                custom_attr_configs=[attr_config(StrMarshaller(), "id", "ID")],
                exclude=["id"],
            )
        )
        customer = Customer("some-id", "Some Name")
        # noinspection PyTestUnpassedFixture
        dumped = context.dump(customer)
        assert "ID" in dumped
        assert "id" not in dumped
        # noinspection PyTestUnpassedFixture
        loaded = context.load(Customer, dumped)
        assert customer == loaded
