"""Automated tests for the Week 11 inventory system changes."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from digital_product import DigitalProduct
from discount_strategy import (
    BulkDiscount,
    DiscountStrategy,
    PercentageDiscount,
    StudentDiscount,
)
from inventory import Inventory
from main import (
    get_positive_float,
    load_products,
    product_from_data,
    product_to_data,
)
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product_factory import ProductFactory
from supplier import Supplier


class Week11Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("SUP-01", "Northstar Supply", "sales@example.com")
        self.physical = ProductFactory.create(
            "physical", "P-100", "Wireless Mouse", 24.99, 18,
            self.supplier, weight=0.2,
        )
        self.digital = ProductFactory.create(
            "digital", "D-200", "Python eBook", 14.50, 50,
            self.supplier, download_size=8.4,
        )

    def test_default_order_strategy_has_no_discount(self) -> None:
        order = Order("ORD-001")
        order.add_order_line(self.physical, 2)
        self.assertAlmostEqual(order.calculate_total(), 49.98)

    def test_percentage_and_bulk_discount_and_strategy_replacement(self) -> None:
        product = ProductFactory.create(
            "physical", "P-250", "Desk", 250, 1, self.supplier
        )
        order = Order("ORD-250", BulkDiscount(200, 20))
        order.add_order_line(product, 1)
        self.assertAlmostEqual(order.calculate_total(), 230)

        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

    def test_new_student_strategy_works_without_order_changes(self) -> None:
        product = ProductFactory.create(
            "digital", "D-100", "Course", 100, 5, self.supplier
        )
        order = Order("ORD-STUDENT", StudentDiscount())
        order.add_order_line(product, 1)
        self.assertAlmostEqual(order.calculate_total(), 95)

    def test_custom_strategy_implements_the_shared_contract(self) -> None:
        class TenDollarDiscount(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total - 10

        order = Order("ORD-CUSTOM", TenDollarDiscount())
        order.add_order_line(self.physical, 1)
        self.assertAlmostEqual(order.calculate_total(), 14.99)

    def test_discount_parameters_are_validated(self) -> None:
        with self.assertRaises(ValueError):
            PercentageDiscount(101)
        with self.assertRaises(ValueError):
            BulkDiscount(-1, 5)
        with self.assertRaises(TypeError):
            Order("ORD-INVALID", "percentage")  # type: ignore[arg-type]

    def test_factory_creates_each_supported_product_type(self) -> None:
        physical = ProductFactory.create(
            "physical", "P-1", "Lamp", 25, 10, self.supplier, weight=1.5
        )
        digital = ProductFactory.create(
            "digital", "D-1", "Editor", 49.9, 100, self.supplier,
            download_size=12.0,
        )
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertEqual(physical.get_weight(), 1.5)
        self.assertEqual(digital.get_download_size(), 12.0)

    def test_factory_rejects_unknown_type(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", "S-1", "Install", 30, 5, self.supplier)

    def test_product_and_order_line_rules_are_enforced(self) -> None:
        for invalid_price in (0, -1):
            with self.subTest(price=invalid_price):
                with self.assertRaisesRegex(ValueError, "Price must be greater"):
                    ProductFactory.create(
                        "digital", "D-X", "Invalid", invalid_price, 1, self.supplier
                    )
        with self.assertRaisesRegex(ValueError, "Stock cannot be negative"):
            ProductFactory.create("physical", "P-X", "Invalid", 1, -1, self.supplier)
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            OrderLine(self.physical, 0)

    def test_get_positive_float_retries_for_text_and_nonpositive_values(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(output):
                result = get_positive_float("Price: ")

        self.assertEqual(result, 12.5)
        self.assertIn("Please enter a valid number, e.g. 12.50.", output.getvalue())
        self.assertIn("Please enter a number greater than zero.", output.getvalue())

    def test_csv_load_skips_bad_rows_and_loads_three_valid_products(self) -> None:
        inventory = Inventory()
        output = io.StringIO()
        csv_path = Path(__file__).resolve().parents[1] / "products.csv"
        with redirect_stdout(output):
            load_products(str(csv_path), inventory, self.supplier)

        message = output.getvalue()
        self.assertEqual(len(inventory.get_products()), 3)
        self.assertIsInstance(inventory.find_product("P001"), PhysicalProduct)
        self.assertIsInstance(inventory.find_product("D001"), DigitalProduct)
        self.assertIsNone(inventory.find_product("S001"))
        self.assertIsNone(inventory.find_product("P002"))
        self.assertIn("Unknown product type: service", message)
        self.assertIn("could not convert string to float: 'abc'", message)
        self.assertIn("3 products loaded.", message)
        self.assertTrue(message.endswith("Load attempt finished.\n"))

    def test_csv_missing_file_is_handled_and_finally_runs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / "missing.csv")
            output = io.StringIO()
            with redirect_stdout(output):
                load_products(missing, Inventory(), self.supplier)

        self.assertEqual(
            output.getvalue(),
            f"Products file not found: {missing}\nLoad attempt finished.\n",
        )

    def test_inventory_serialization_keeps_types_and_supplier_reference(self) -> None:
        records = [product_to_data(self.physical), product_to_data(self.digital)]
        cache: dict[str, Supplier] = {}
        restored = [product_from_data(record, cache) for record in records]
        self.assertIsInstance(restored[0], PhysicalProduct)
        self.assertIsInstance(restored[1], DigitalProduct)
        self.assertIs(restored[0].get_supplier(), restored[1].get_supplier())

    def test_inventory_accepts_transferable_product_and_rejects_duplicates(self) -> None:
        inventory = Inventory()
        self.assertTrue(inventory.add_product(self.physical))
        self.assertFalse(inventory.add_product(self.physical))
        self.assertIs(inventory.find_product("P-100"), self.physical)


if __name__ == "__main__":
    unittest.main()
