"""Main program for the Week 8 object-oriented inventory system."""

import json
import os

from inventory import Inventory
from product import Product


INVENTORY_FILE = "inventory.json"


def load_inventory():
    """Load product information from the JSON file."""
    inventory = Inventory()

    if not os.path.exists(INVENTORY_FILE):
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory

    try:
        with open(INVENTORY_FILE, "r") as file:
            product_list = json.load(file)

        for product_data in product_list:
            product = Product(
                product_data["id"],
                product_data["name"],
                product_data["price"],
                product_data["stock"],
            )
            if not inventory.add_product(product):
                raise ValueError("Duplicate product ID: " + product.get_product_id())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Could not load inventory: " + str(error))
        return None

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    """Save product information to the JSON file."""
    product_list = []

    for product in inventory.get_products():
        product_data = {
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
        }
        product_list.append(product_data)

    try:
        with open(INVENTORY_FILE, "w") as file:
            json.dump(product_list, file, indent=4)
        print("Inventory saved successfully to inventory.json.")
    except OSError as error:
        print("Could not save inventory: " + str(error))


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
        product = Product(product_id, name, price, stock)
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

    print("Current product information:")
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
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("------------------------------------------------")
    product.display_information()
    print("------------------------------------------------")


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


main()
