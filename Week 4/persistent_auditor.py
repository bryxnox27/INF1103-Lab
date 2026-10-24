def load_inventory():
    inventory_records = []
    history = []
    total_inventory = 0

    try:
        with open("inventory.txt", "r") as file:
            for line in file:
                line = line.strip()

                if line != "":
                    parts = line.split(",")

                    if len(parts) == 3:
                        item_id = int(parts[0].strip())
                        product_name = parts[1].strip()
                        quantity = int(parts[2].strip())

                        inventory_records.append([item_id, product_name, quantity])
                        history.append(quantity)
                        total_inventory += quantity

    except FileNotFoundError:
        print("No inventory file found. Starting with empty inventory.")

    return inventory_records, total_inventory, history

def save_inventory(inventory_records):
    with open("inventory.txt", "w") as file:
        for record in inventory_records:
            file.write(f"{record[0]},{record[1]},{record[2]}\n")

def display_inventory(inventory_records):
    print("Current Orders:\n")

    if len(inventory_records) == 0:
        print("No records found.")
    else:
        for record in inventory_records:
            print(f"{record[0]}, {record[1]}, {record[2]}")

def get_product_name():
    name = input("\nEnter Product Name (or type quit): ").strip()

    if name.lower() == "quit":
        return "quit"

    if name == "":
        return None

    return name

def get_valid_quantity():
    entry = input("Enter Quantity (or type quit): ").strip()

    if entry.lower() == "quit":
        return "quit"

    try:
        value = int(entry)
        if value < 0:
            raise ValueError
        return value
    except ValueError:
        return None

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def get_next_item_id(inventory_records):
    if len(inventory_records) == 0:
        return 1001

    return int(inventory_records[-1][0]) + 1

def generate_report(total_units, failed_attempts, total_inventory, history):
    print("\nFinal Report")
    print("----------------------------")
    print("Final Inventory Level:", total_inventory)
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)
    print("Transaction History:", history)

def main():
    inventory_records, total_inventory, history = load_inventory()
    deliveries_processed = 0
    failed_attempts = 0

    display_inventory(inventory_records)
    print(f"\nCurrent Total Inventory: {total_inventory}")
    print(f"Loaded Transaction History: {history}")

    while True:
        product_name = get_product_name()

        if product_name == "quit":
            save_inventory(inventory_records)
            print("\nInventory successfully saved to inventory.txt")
            break

        if product_name is None:
            failed_attempts += 1
            print("Invalid product name. Please try again.")
            continue

        quantity = get_valid_quantity()

        if quantity == "quit":
            save_inventory(inventory_records)
            print("\nInventory successfully saved to inventory.txt")
            break

        if quantity is None:
            failed_attempts += 1
            print("Invalid quantity. Please try again.")
            continue

        new_item_id = get_next_item_id(inventory_records)
        new_record = [new_item_id, product_name, quantity]

        inventory_records.append(new_record)
        history.append(quantity)
        total_inventory = process_delivery(total_inventory, quantity)

        tax = calculate_tax(quantity)
        deliveries_processed += 1

        print("\nNew Order Added:")
        print(f"{new_record[0]}, {new_record[1]}, {new_record[2]}")
        print(f"Tax: ${tax:.2f}")
        print(f"SKU Quantity: {new_record[2]} | Updated Inventory Level: {total_inventory}")

    generate_report(deliveries_processed, failed_attempts, total_inventory, history)

main()
