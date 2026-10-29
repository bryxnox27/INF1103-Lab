"""Command-line inventory application with physical and digital products."""

import json
import os

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct


INVENTORY_FILE = "inventory.json"


def product_from_data(data):
    """Build the correct subclass from one saved JSON record."""
    common = (data["id"], data["name"], data["price"], data["stock"])
    product_type = data["type"].lower()
    if product_type == "physical":
        return PhysicalProduct(*common, data["weight"])
    if product_type == "digital":
        return DigitalProduct(*common, data["download_size"])
    raise ValueError("Unknown product type: " + product_type)


def product_to_data(product):
    """Convert a product object to a JSON-compatible dictionary."""
    data = {
        "type": "physical" if isinstance(product, PhysicalProduct) else "digital",
        "id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock": product.get_stock(),
    }
    if isinstance(product, PhysicalProduct):
        data["weight"] = product.get_weight()
    else:
        data["download_size"] = product.get_download_size()
    return data


def load_inventory():
    """Load products and preserve their concrete product types."""
    inventory = Inventory()
    if not os.path.exists(INVENTORY_FILE):
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory

    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
            product_list = json.load(file)
        if not isinstance(product_list, list):
            raise ValueError("Inventory data must be a list.")
        for product_data in product_list:
            product = product_from_data(product_data)
            if not inventory.add_product(product):
                raise ValueError("Duplicate product ID: " + product.get_product_id())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Could not load inventory: " + str(error))
        return None

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    """Save product types and type-specific fields to JSON."""
    try:
        with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(
                [product_to_data(product) for product in inventory.get_products()],
                file,
                indent=4,
            )
        print("Inventory saved successfully to inventory.json.")
    except OSError as error:
        print("Could not save inventory: " + str(error))


def add_product(inventory):
    print("\nAdd New Product")
    product_type = input("Product type (1=Physical, 2=Digital): ").strip()
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
        if product_type == "1":
            weight = float(input("Weight in kg: ").strip())
            product = PhysicalProduct(product_id, name, price, stock, weight)
        elif product_type == "2":
            size = float(input("Download size in MB: ").strip())
            product = DigitalProduct(product_id, name, price, stock, size)
        else:
            print("Invalid product type.")
            return
    except ValueError as error:
        print("Invalid product details: " + str(error))
        return

    if not inventory.add_product(product):
        print("Product ID already exists.")
        return
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
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


def search_product(inventory):
    print("\nSearch Product")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return
    print("\nProduct Found")
    product.display_information()
    print("Fulfilment: " + product.get_fulfilment_info())
    if isinstance(product, PhysicalProduct):
        print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")


def display_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")
    inventory = load_inventory()
    if inventory is None:
        return

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
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

