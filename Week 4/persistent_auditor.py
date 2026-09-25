def get_valid_input():
    entry = input("Enter stock quantity (or type quit): ").strip()

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

def generate_report(total_units, failed_attempts, inventory, history):
    print("\n--- Inventory Report ---")
    print("Final Inventory Level:", inventory)
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)
    print("Transaction History:", history)

def load_inventory():
    inventory = 0
    history = []

    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()

                if line.startswith("Inventory:"):
                    inventory_text = line.replace("Inventory:", "").strip()
                    if inventory_text:
                        inventory = int(inventory_text)

                elif line.startswith("History:"):
                    history_text = line.replace("History:", "").strip()
                    if history_text:
                        history = [int(item) for item in history_text.split(",")]

    except FileNotFoundError:
        print("No inventory file found. Starting with empty inventory.")

    return inventory, history

def save_inventory(inventory, history):
    with open("inventory.txt", "w") as file:
        file.write(f"Inventory: {inventory}\n")
        file.write("History: " + ",".join(str(item) for item in history) + "\n")

def main():
    inventory, history = load_inventory()
    deliveries_processed = 0
    failed_attempts = 0

    print("Starting Inventory Level:", inventory)
    print("Loaded Transaction History:", history)

    while True:
        delivery = get_valid_input()

        if delivery == "quit":
            save_inventory(inventory, history)
            print("Inventory data saved to inventory.txt")
            break

        if delivery is None:
            failed_attempts += 1
            print("Invalid entry. Please try again.")
            continue

        inventory = process_delivery(inventory, delivery)
        tax = calculate_tax(delivery)
        deliveries_processed += 1
        history.append(delivery)

        print(f"Tax for this delivery: ${tax:.2f}")
        print(f"Updated Inventory Level: {inventory}")

    generate_report(deliveries_processed, failed_attempts, inventory, history)

main()
