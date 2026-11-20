"""Inventory Management System for INF1103 Week 11."""

import csv
import json
import math
import os
from collections.abc import Mapping

from digital_product import DigitalProduct
from discount_strategy import (
    BulkDiscount,
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    StudentDiscount,
)
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from shipping import CanBeShipped
from supplier import Supplier


INVENTORY_FILE = "inventory.json"
PRODUCTS_FILE = "products.csv"
ProductRecord = Mapping[str, object]


def supplier_from_data(
    data: ProductRecord,
    product_id: str,
    supplier_cache: dict[str, Supplier],
) -> Supplier:
    """Load a supplier and reuse one object for records with the same ID."""
    raw_supplier = data.get("supplier")
    if isinstance(raw_supplier, Mapping):
        supplier_id = str(raw_supplier.get("supplier_id", f"LEGACY-{product_id}"))
        name = str(raw_supplier.get("name", "Legacy supplier"))
        contact_email = str(
            raw_supplier.get("contact_email", "legacy@example.com")
        )
    else:
        # Support Week 9 JSON records that predate the Supplier association.
        supplier_id = f"LEGACY-{product_id}"
        name = "Legacy supplier"
        contact_email = "legacy@example.com"

    existing = supplier_cache.get(supplier_id)
    if existing is not None:
        if (
            existing.get_name() != name
            or existing.get_contact_email() != contact_email
        ):
            raise ValueError(
                f"Supplier ID {supplier_id} has conflicting saved details."
            )
        return existing

    supplier = Supplier(supplier_id, name, contact_email)
    supplier_cache[supplier_id] = supplier
    return supplier


def product_from_data(
    data: ProductRecord,
    supplier_cache: dict[str, Supplier] | None = None,
) -> Product:
    """Build a product from saved fields through ProductFactory."""
    product_id = str(data["id"])
    if supplier_cache is None:
        supplier_cache = {}
    supplier = supplier_from_data(data, product_id, supplier_cache)
    product_type = str(data["type"])

    attributes: dict[str, float] = {}
    if product_type.strip().lower() == "physical":
        attributes["weight"] = float(data.get("weight", 0.0))
    elif product_type.strip().lower() == "digital":
        attributes["download_size"] = float(data.get("download_size", 0.0))

    return ProductFactory.create(
        product_type,
        product_id,
        str(data["name"]),
        float(data["price"]),
        int(data["stock"]),
        supplier,
        **attributes,
    )


def product_to_data(product: Product) -> dict[str, object]:
    """Convert a Product and its Supplier to a JSON-compatible record."""
    supplier = product.get_supplier()
    data: dict[str, object] = {
        "id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock": product.get_stock(),
        "supplier": {
            "supplier_id": supplier.get_supplier_id(),
            "name": supplier.get_name(),
            "contact_email": supplier.get_contact_email(),
        },
    }
    if isinstance(product, PhysicalProduct):
        data["type"] = "physical"
        data["weight"] = product.get_weight()
    elif isinstance(product, DigitalProduct):
        data["type"] = "digital"
        data["download_size"] = product.get_download_size()
    else:
        raise TypeError(f"Unsupported Product subclass: {type(product).__name__}")
    return data


def load_inventory(filename: str = INVENTORY_FILE) -> Inventory | None:
    """Load saved products and preserve their types and shared suppliers."""
    inventory = Inventory()
    if not os.path.exists(filename):
        print(f"{filename} not found. Starting with an empty inventory.")
        return inventory

    try:
        with open(filename, "r", encoding="utf-8") as file:
            product_list = json.load(file)
        if not isinstance(product_list, list):
            raise ValueError("Inventory data must be a list.")

        supplier_cache: dict[str, Supplier] = {}
        for product_data in product_list:
            if not isinstance(product_data, Mapping):
                raise ValueError("Each inventory record must be an object.")
            product = product_from_data(product_data, supplier_cache)
            if not inventory.add_product(product):
                raise ValueError("Duplicate product ID: " + product.get_product_id())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Could not load inventory: " + str(error))
        return None

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(
    inventory: Inventory,
    filename: str = INVENTORY_FILE,
) -> None:
    """Save products with their concrete type and supplier details."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [product_to_data(product) for product in inventory.get_products()],
                file,
                indent=4,
            )
        print(f"Inventory saved successfully to {filename}.")
    except (OSError, TypeError, ValueError) as error:
        print("Could not save inventory: " + str(error))


def _validate_positive_price(value: float) -> None:
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Price must be greater than zero.")


def get_positive_float(prompt: str) -> float:
    """Ask until the user enters a number greater than zero."""
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number, e.g. 12.50.")
            continue

        try:
            _validate_positive_price(value)
        except ValueError:
            print("Please enter a number greater than zero.")
            continue
        return value


def find_supplier(inventory: Inventory, supplier_id: str) -> Supplier | None:
    """Reuse an existing Supplier object when its ID is already in inventory."""
    supplier_id = str(supplier_id).strip()
    for product in inventory.get_products():
        supplier = product.get_supplier()
        if supplier.get_supplier_id() == supplier_id:
            return supplier
    return None


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_type = input("Product type (1=Physical, 2=Digital): ").strip()
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()

    try:
        price = get_positive_float("Price: ")
        stock = int(input("Stock Quantity: ").strip())
        supplier_id = input("Supplier ID: ").strip()
        supplier_name = input("Supplier Name: ").strip()
        supplier_email = input("Supplier Contact Email: ").strip()
        supplier = find_supplier(inventory, supplier_id)
        if supplier is None:
            supplier = Supplier(supplier_id, supplier_name, supplier_email)
        elif (
            supplier.get_name() != supplier_name
            or supplier.get_contact_email() != supplier_email
        ):
            print("That Supplier ID already exists with different details.")
            return

        attributes: dict[str, float] = {}
        if product_type == "1":
            attributes["weight"] = float(input("Weight in kg: ").strip())
            product_kind = "physical"
        elif product_type == "2":
            attributes["download_size"] = float(
                input("Download size in MB: ").strip()
            )
            product_kind = "digital"
        else:
            print("Invalid product type.")
            return

        product = ProductFactory.create(
            product_kind,
            product_id,
            name,
            price,
            stock,
            supplier,
            **attributes,
        )
    except (ValueError, TypeError) as error:
        print("Invalid product details: " + str(error))
        return

    if not inventory.add_product(product):
        print("Product ID already exists.")
        return
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    product.display_information()
    try:
        quantity = int(input("New Stock Quantity: ").strip())
        inventory.update_stock(product_id, quantity)
    except ValueError as error:
        print("Invalid stock quantity: " + str(error))
        return
    print("Stock updated successfully!")


def show_product_details(product: Product) -> None:
    """Use behavior promised by Product; subclasses supply the details."""
    product.display_information()
    print("Fulfilment: " + product.get_fulfilment_info())


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.find_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    show_product_details(product)
    if isinstance(product, CanBeShipped):
        print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")


def _choose_discount() -> DiscountStrategy:
    """Create a discount selected for one order."""
    choice = input(
        "Discount (blank=None, percentage, bulk, student): "
    ).strip().lower()
    if not choice:
        return NoDiscount()
    if choice == "percentage":
        return PercentageDiscount(float(input("Discount percent: ").strip()))
    if choice == "bulk":
        threshold = float(input("Bulk threshold: ").strip())
        amount = float(input("Discount amount: ").strip())
        return BulkDiscount(threshold, amount)
    if choice == "student":
        return StudentDiscount()
    raise ValueError("Choose percentage, bulk, student, or leave blank.")


def create_order(inventory: Inventory) -> None:
    """Build an Order from existing inventory products."""
    order_id = input("Order ID: ").strip()
    try:
        order = Order(order_id)
    except ValueError as error:
        print("Invalid order: " + str(error))
        return

    print("Enter a product ID and quantity. Leave the product ID blank to finish.")
    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        try:
            quantity = int(input("Quantity: ").strip())
            order.add_order_line(product, quantity)
        except ValueError as error:
            print("Invalid order line: " + str(error))

    try:
        order.set_discount(_choose_discount())
    except (ValueError, TypeError) as error:
        print("Invalid discount; using no discount: " + str(error))
        order.set_discount(NoDiscount())
    order.display_order_lines()


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Import CSV rows, reporting and skipping rows that fail validation."""
    loaded = 0
    try:
        product_file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with product_file:
            rows = csv.reader(product_file)
            next(rows, None)  # Skip the header row.
            for line_number, row in enumerate(rows, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError("Expected five comma-separated fields.")
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        price,
                        stock_quantity,
                        supplier,
                    )
                    if not inventory.add_product(product):
                        raise ValueError(f"Duplicate product ID: {product_id}")
                except ValueError as error:
                    print(f"Skipping row {line_number}: {error}")
                else:
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def display_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("7. Create Order")
    print("8. Load Products from CSV")
    print("----------------------------")


def main() -> None:
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")
    inventory = load_inventory()
    if inventory is None:
        return

    csv_supplier = Supplier(
        "SUP-CSV", "CSV Import Supplier", "imports@example.com"
    )
    while True:
        display_menu()
        choice = input("\nEnter option: ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        elif choice == "7":
            create_order(inventory)
        elif choice == "8":
            load_products(PRODUCTS_FILE, inventory, csv_supplier)
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
