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


def generate_report(total_units, failed_attempts):
	print("Total Deliveries Processed:", total_units)
	print("Number of Failed/Rejected Entries:", failed_attempts)

inventory = 0
deliveries_processed = 0
failed_attempts = 0

while True:
    delivery = get_valid_input()
    if delivery == "quit":
        break
    if delivery is None:
        failed_attempts += 1
        print("Invalid entry. Please try again.")
        continue

    inventory = process_delivery(inventory, delivery)
    tax = calculate_tax(delivery)
    deliveries_processed += 1
    print(f"Tax for this delivery: ${tax:.2f}")

generate_report(deliveries_processed, failed_attempts)

