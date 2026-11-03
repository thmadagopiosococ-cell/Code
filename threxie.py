from datetime import datetime
import json

items = []
next_id = 1


def load_data():
    global items, next_id
    try:
        with open("lost_and_found_data.json", "r") as f:
            data = json.load(f)
            items = data.get("items", [])
            next_id = data.get("next_id", 1)
    except Exception:
        items = []
        next_id = 1


def save_data():
    data = {
        "items": items,
        "next_id": next_id
    }
    with open("lost_and_found_data.json", "w") as f:
        json.dump(data, f, indent=4)


def add_item():
    global next_id

    print("\n--- ADD ITEM ---")

    # Report Type (Lost or Found)
    while True:
        report_type = input("Enter report type (Lost/Found): ").strip().capitalize()
        if report_type in ["Lost", "Found"]:
            break
        print("Invalid choice. Please enter either 'Lost' or 'Found'.")

    # Category (what kind of item it is)
    while True:
        category = input("Enter item category (e.g., Electronics, Clothing, ID/Cards): ").strip()
        if category:
            break
        print("Category cannot be empty. Please try again.")

    while True:
        name = input("Enter item name: ").strip()
        if name:
            break
        print("Item name cannot be empty. Please try again.")

    brand = input("Enter brand (optional): ").strip()
    color = input("Enter color (optional): ").strip()
    description = input("Enter description: ").strip()
    location = input("Enter location: ").strip()

    # Date validation loop (only re-prompts date if invalid)
    while True:
        date_input = input("Enter date (MM/DD/YYYY): ").strip()
        try:
            entered_date = datetime.strptime(date_input, "%m/%d/%Y").date()
            current_date = datetime.now().date()

            if entered_date > current_date:
                print("Invalid date. Future dates are not accepted. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY.")

    # Contact validation loop (only re-prompts contact if invalid)
    while True:
        contact = input("Enter contact number (digits only): ").strip()
        if contact.isdigit():
            break
        print("Invalid contact number. Letters and special characters are not allowed. Please try again.")

    item = {
        "id": next_id,
        "report_type": report_type,
        "category": category,
        "name": name,
        "brand": brand if brand else "N/A",
        "color": color if color else "N/A",
        "description": description if description else "N/A",
        "location": location if location else "N/A",
        "date": date_input,
        "contact": contact,
        "status": "Unclaimed",
        "claimant_name": "N/A",
        "claimant_section": "N/A",
        "claimant_contact": "N/A"
    }

    items.append(item)
    next_id += 1
    save_data()

    print("\nItem added successfully!")


def view_items():
    print("\n--- LOST AND FOUND ITEMS ---")

    if not items:
        print("No items recorded.")
        return

    # Table Header
    header = f"{'ID':<4} | {'Type':<6} | {'Category':<12} | {'Item Name':<12} | {'Brand':<10} | {'Color':<8} | {'Location':<12} | {'Status':<9}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    # Table Rows
    for item in items:
        report_type = item.get("report_type", "Lost")
        category = item.get("category", "N/A")
        print(f"{item['id']:<4} | {report_type:<6} | {category:<12} | {item['name']:<12} | {item['brand']:<10} | {item['color']:<8} | {item['location']:<12} | {item['status']:<9}")
    
    print("-" * len(header))


def search_update_item():
    print("\n--- SEARCH / UPDATE ITEM ---")

    keyword = input("Enter item name or keyword: ").strip().lower()
    found_items = []

    for item in items:
        if (keyword in item["name"].lower()
                or keyword in item["description"].lower()
                or keyword in item["brand"].lower()
                or keyword in item["color"].lower()
                or keyword in item["category"].lower()):
            found_items.append(item)

    if not found_items:
        print("No matching item found.")
        return

    print("\nMatching items:")
    for item in found_items:
        print(f"\nID: {item['id']}")
        print(f"Report Type: {item.get('report_type', 'Lost')}")
        print(f"Category: {item['category']}")
        print(f"Item Name: {item['name']}")
        print(f"Brand: {item['brand']}")
        print(f"Color: {item['color']}")
        print(f"Description: {item['description']}")
        print(f"Location: {item['location']}")
        print(f"Date: {item['date']}")
        print(f"Status: {item['status']}")
        if item["status"] == "Claimed":
            print(f"Claimant Name: {item.get('claimant_name', 'N/A')}")
            print(f"Claimant Section: {item.get('claimant_section', 'N/A')}")
            print(f"Claimant Contact: {item.get('claimant_contact', 'N/A')}")

    try:
        item_id = int(input("\nEnter ID of the item you want to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    for item in items:
        if item["id"] == item_id:
            print("\nLeave blank if you do not want to change the information.")

            report_type_input = input(f"Report Type (Lost/Found) [{item.get('report_type', 'Lost')}]: ").strip().capitalize()
            category = input(f"Category [{item['category']}]: ").strip()
            name = input(f"Item Name [{item['name']}]: ").strip()
            brand = input(f"Brand [{item['brand']}]: ").strip()
            color = input(f"Color [{item['color']}]: ").strip()
            description = input(f"Description [{item['description']}]: ").strip()
            location = input(f"Location [{item['location']}]: ").strip()
            status = input(f"Status [{item['status']}]: ").strip().capitalize()

            if report_type_input in ["Lost", "Found"]:
                item["report_type"] = report_type_input
            if category:
                item["category"] = category
            if name:
                item["name"] = name
            if brand:
                item["brand"] = brand
            if color:
                item["color"] = color
            if description:
                item["description"] = description
            if location:
                item["location"] = location
            if status in ["Unclaimed", "Claimed"]:
                item["status"] = status

            # Contact update validation loop
            while True:
                contact_input = input(f"Contact [{item['contact']}]: ").strip()
                if not contact_input:
                    break
                if contact_input.isdigit():
                    item["contact"] = contact_input
                    break
                else:
                    print("Invalid contact format. Digits only. Try again or leave blank to skip.")

            save_data()
            print("Item updated successfully!")
            return

    print("Item ID not found.")


def claim_item():
    print("\n--- CLAIM ITEM ---")

    try:
        item_id = int(input("Enter item ID to claim: "))
    except ValueError:
        print("Invalid ID.")
        return

    for item in items:
        if item["id"] == item_id:
            if item["status"] == "Claimed":
                print("This item has already been claimed.")
                print(f"Claimed by: {item.get('claimant_name', 'N/A')} | Section: {item.get('claimant_section', 'N/A')}")
            else:
                print("\n--- Enter Claimant Information ---")
                
                while True:
                    claimant_name = input("Enter claimant's name: ").strip()
                    if claimant_name:
                        break
                    print("Name cannot be empty. Please try again.")

                while True:
                    claimant_section = input("Enter claimant's section: ").strip()
                    if claimant_section:
                        break
                    print("Section cannot be empty. Please try again.")

                while True:
                    claimant_contact = input("Enter claimant's contact number (digits only): ").strip()
                    if claimant_contact.isdigit():
                        break
                    print("Invalid contact number. Digits only. Please try again.")

                item["status"] = "Claimed"
                item["claimant_name"] = claimant_name
                item["claimant_section"] = claimant_section
                item["claimant_contact"] = claimant_contact

                save_data()
                print("\nItem successfully marked as claimed with claimant details recorded!")
            return

    print("Item ID not found.")


def delete_item():
    print("\n--- DELETE ITEM ---")

    try:
        item_id = int(input("Enter item ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            save_data()
            print("Item deleted successfully!")
            return

    print("Item ID not found.")


def main():
    load_data()
    while True:
        print("\n======================================")
        print("  LOST AND FOUND MANAGEMENT SYSTEM")
        print("======================================")
        print("1. Add Item")
        print("2. View All Items")
        print("3. Search / Update Item")
        print("4. Claim Item")
        print("5. Delete Item")
        print("6. Exit")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_item()
        elif choice == "2":
            view_items()
        elif choice == "3":
            search_update_item()
        elif choice == "4":
            claim_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            save_data()
            print("\nThank you for using the Lost and Found Management System!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()