"""Small console demonstration of the Week 10 object relationships."""

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> None:
    """Call Product operations without checking the concrete subclass."""
    product.display_information()
    print("Fulfilment: " + product.get_fulfilment_info())


def display_inventory_details(inventory: Inventory) -> None:
    """Demonstrate one polymorphic loop over Product references."""
    for product in inventory.get_products():
        show_product_details(product)


def main() -> None:
    supplier = Supplier("SUP-01", "Northstar Supply", "sales@example.com")
    physical = PhysicalProduct(
        "P-100", "Wireless Mouse", 24.99, 18, supplier, 0.2
    )
    digital = DigitalProduct(
        "D-200", "Python eBook", 14.50, 50, supplier, 8.4
    )

    print("Supplier information through each Product")
    physical.display_supplier_information()
    digital.display_supplier_information()

    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(physical)
    inventory_a.add_product(digital)
    print("\nProducts in one Inventory")
    display_inventory_details(inventory_a)

    inventory_a.remove_product(physical.get_product_id())
    inventory_b.add_product(physical)
    print("\nThe same Product object was transferred to Inventory B")
    print(f"Still usable: {physical.get_name()} ({physical.get_stock()} in stock)")

    order_one = Order("ORD-001")
    order_two = Order("ORD-002")
    order_one.add_order_line(physical, 2)
    order_two.add_order_line(physical, 1)
    print("\nEach Order created its own OrderLine")
    print(f"Order 1 lines: {len(order_one.order_lines)}")
    print(f"Order 2 lines: {len(order_two.order_lines)}")
    same_product = (
        order_one.order_lines[0].product is order_two.order_lines[0].product
    )
    same_line = order_one.order_lines[0] is order_two.order_lines[0]
    print(f"Same Product reference: {same_product}")
    print(f"Same OrderLine object: {same_line}")
    order_one.display_order_lines()
    order_two.display_order_lines()


if __name__ == "__main__":
    main()
