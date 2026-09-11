inventory = 0
failed_entries = 0

while True:
	entry = input("Enter stock quantity (or type quit): ").strip()

	if entry.lower() == "quit":
		break

	if entry.startswith("-"):
		print("Error: negative stock quantities are not allowed.")
		failed_entries += 1
		continue

	if not entry.isdigit():
		print("Error: enter a whole number.")
		failed_entries += 1
		continue

	inventory += int(entry)

	if inventory > 500:
		print("Alert: inventory exceeds storage capacity!")
		break

print(f"Total Units Processed: {inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")

