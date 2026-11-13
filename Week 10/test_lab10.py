"""Submission checks for Week 10 relationships and substitutability."""

import io
import unittest
from contextlib import redirect_stdout

from digital_product import DigitalProduct
from inventory import Inventory
from lab10_demo import show_product_details
from main import product_from_data, product_to_data
from order import Order
from physical_product import PhysicalProduct
from supplier import Supplier


class Week10RelationshipTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("SUP-01", "Northstar Supply", "sales@example.com")
        self.physical = PhysicalProduct(
            "P-100", "Wireless Mouse", 24.99, 18, self.supplier, 0.2
        )
        self.digital = DigitalProduct(
            "D-200", "Python eBook", 14.50, 50, self.supplier, 8.4
        )

    def test_product_keeps_supplier_reference(self) -> None:
        self.assertIs(self.physical.get_supplier(), self.supplier)
        self.assertIs(self.digital.get_supplier(), self.supplier)

        del self.supplier
        output = io.StringIO()
        with redirect_stdout(output):
            self.physical.display_supplier_information()
            self.digital.display_supplier_information()
        self.assertEqual(output.getvalue().count("Northstar Supply"), 2)

    def test_inventory_aggregates_transferable_products(self) -> None:
        product = self.physical
        inventory_a = Inventory()
        inventory_b = Inventory()

        self.assertTrue(inventory_a.add_product(product))
        self.assertIs(inventory_a.find_product("P-100"), product)
        self.assertTrue(inventory_a.remove_product("P-100"))
        self.assertEqual(product.get_name(), "Wireless Mouse")
        self.assertTrue(inventory_b.add_product(product))
        self.assertIs(inventory_b.find_product("P-100"), product)
        self.assertFalse(inventory_a.remove_product("missing"))

    def test_orders_create_distinct_lines_for_shared_product(self) -> None:
        first_order = Order("ORD-001")
        second_order = Order("ORD-002")
        first_order.add_order_line(self.physical, 2)
        second_order.add_order_line(self.physical, 1)

        first_line = first_order.order_lines[0]
        second_line = second_order.order_lines[0]
        self.assertIsNot(first_line, second_line)
        self.assertIs(first_line.product, second_line.product)
        self.assertAlmostEqual(first_line.calculate_subtotal(), 49.98)
        self.assertAlmostEqual(first_order.calculate_total(), 49.98)
        self.assertTrue(first_order.remove_order_line("P-100"))
        self.assertEqual(first_order.order_lines, [])
        self.assertEqual(len(second_order.order_lines), 1)

    def test_both_subclasses_work_through_product_operations(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)

        output = io.StringIO()
        with redirect_stdout(output):
            for product in inventory.get_products():
                show_product_details(product)

        displayed = output.getvalue()
        self.assertIn("This product requires physical shipping.", displayed)
        self.assertIn("This product is delivered digitally.", displayed)

    def test_both_subclasses_preserve_stock_behavior(self) -> None:
        self.physical.update_stock(7)
        self.digital.update_stock(12)
        self.assertEqual(self.physical.get_stock(), 7)
        self.assertEqual(self.digital.get_stock(), 12)

    def test_json_round_trip_preserves_supplier_and_product_types(self) -> None:
        records = [product_to_data(self.physical), product_to_data(self.digital)]
        supplier_cache: dict[str, Supplier] = {}
        restored = [
            product_from_data(record, supplier_cache) for record in records
        ]

        self.assertIsInstance(restored[0], PhysicalProduct)
        self.assertIsInstance(restored[1], DigitalProduct)
        self.assertEqual(
            restored[0].get_supplier().get_contact_email(), "sales@example.com"
        )
        self.assertIs(restored[0].get_supplier(), restored[1].get_supplier())

    def test_week9_json_without_supplier_still_loads(self) -> None:
        legacy_record: dict[str, object] = {
            "type": "digital",
            "id": "D-OLD",
            "name": "Legacy eBook",
            "price": 5.0,
            "stock": 2,
            "download_size": 1.2,
        }
        product = product_from_data(legacy_record)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_supplier().get_supplier_id(), "LEGACY-D-OLD")


if __name__ == "__main__":
    unittest.main()
