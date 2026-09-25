inventory = 0

while True:
	entry = input("Enter stock quantity (or type 'quit'): ").strip()

	if entry.lower() == "quit":
		print(f"Total inventory: {inventory}")
		break

	if not entry.isdigit():
		print("Error: please enter a non-negative whole number.")
		continue

	quantity = int(entry)
	if quantity < 0:
		print("Error: stock quantity cannot be negative.")
		continue

	inventory += quantity

	if inventory > 500:
		print("Alert: inventory exceeds storage capacity.")
		break
