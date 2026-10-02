import json
import os

def load_inventory():
    if os.path.exists("inventory.json"):
        print("inventory.json found.")
        with open("inventory.json", "r") as file:
            inventory = json.load(file)
        print("Inventory loaded successfully.")
    else:
        print("inventory.json not found.")
        print("Starting with default inventory.")
        inventory = [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
        ]
    return inventory

def save_inventory(inventory):
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)
    print("Inventory saved successfully to inventory.json.")

def display_all(inventory):
    print("\nCurrent Inventory")
    print("------------------------------------------------")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | Price: \${product['price']:.2f} | Stock: {product['stock']}")
    print("------------------------------------------------")

def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    product_name = input("Product Name: ").strip()

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("Invalid price or stock quantity.")
        return

    for product in inventory:
        if product["id"] == product_id:
            print("Product ID already exists.")
            return

    new_product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    inventory.append(new_product)
    print("\nProduct added successfully!")

def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    for product in inventory:
        if product["id"] == product_id:
            print("\nProduct Found")
            print("------------------------------------------------")
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: \${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("------------------------------------------------")
            return product

    print("\nProduct not found.")
    return None


