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



def generate_report(total_units, failed_attempts, total_inventory, history):
    print("\nFinal Report:")
    print("Final Inventory Level:", total_inventory)
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)
    print("Transaction History:", history)

def main():
    inventory_records, total_inventory, history = load_inventory()


    generate_report(total_inventory, history)

main()
