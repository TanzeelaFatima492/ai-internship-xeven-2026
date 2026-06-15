import json

contacts = {}
next_id = 1

def add_contact():
    global next_id

    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email: ")

    contacts[next_id] = {
        "name": name,
        "phone": phone,
        "email": email,
        "tags": set(),
        "notes": []
    }

    print(f"Contact added with ID: {next_id}")
    next_id += 1

def search_contacts():
    keyword = input("Search by name/phone/email: ").lower()

    results = [
        (cid, data)
        for cid, data in contacts.items()
        if keyword in data["name"].lower()
        or keyword in data["phone"].lower()
        or keyword in data["email"].lower()
    ]

    if results:
        for cid, data in results:
            print(f"ID: {cid}, Name: {data['name']}, Phone: {data['phone']}, Email: {data['email']}, Tags: {data['tags']}")
    else:
        print("No contacts found.")

def update_contact():
    cid = int(input("Enter contact ID: "))

    if cid in contacts:
        name = input("New name: ")
        phone = input("New phone: ")
        email = input("New email: ")

        contacts[cid]["name"] = name
        contacts[cid]["phone"] = phone
        contacts[cid]["email"] = email

        print("Contact updated.")
    else:
        print("Contact not found.")

def delete_contact():
    cid = int(input("Enter contact ID: "))

    if cid in contacts:
        del contacts[cid]
        print("Contact deleted.")
    else:
        print("Contact not found.")


def add_tag():
    cid = int(input("Contact ID: "))
    tag = input("Enter tag: ")

    if cid in contacts:
        contacts[cid]["tags"].add(tag)
        print("Tag added.")
    else:
        print("Contact not found.")


def remove_tag():
    cid = int(input("Contact ID: "))
    tag = input("Enter tag to remove: ")

    if cid in contacts:
        contacts[cid]["tags"].discard(tag)
        print("Tag removed.")
    else:
        print("Contact not found.")


def find_by_tag():
    tag = input("Enter tag: ")

    results = [
        (cid, data)
        for cid, data in contacts.items()
        if tag in data["tags"]
    ]

    if results:
        for cid, data in results:
            print(f"ID: {cid}, Name: {data['name']}, Phone: {data['phone']}, Email: {data['email']}, Tags: {data['tags']}")
    else:
        print("No contacts with this tag.")

def save_contacts():
    try:
        with open("contacts.json", "w") as f:
            json.dump(
                {
                    cid: {
                        **data,
                        "tags": list(data["tags"])  # convert set to list
                    }
                    for cid, data in contacts.items()
                },
                f
            )
        print("Contacts saved.")
    except Exception as e:
        print("Error saving:", e)


def load_contacts():
    global contacts, next_id

    try:
        with open("contacts.json", "r") as f:
            data = json.load(f)

            contacts = {
                int(cid): {
                    **info,
                    "tags": set(info["tags"]),
                    "notes": info.get("notes", [])
                }
                for cid, info in data.items()
            }

            next_id = max(contacts.keys(), default=0) + 1

        print("Contacts loaded.")
    except FileNotFoundError:
        print("No saved file found.")
    except Exception as e:
        print("Error loading:", e)


def show_stats():
    total = len(contacts)

    tag_count = {}
    for data in contacts.values():
        for tag in data["tags"]:
            tag_count[tag] = tag_count.get(tag, 0) + 1

    most_used = max(tag_count, key=tag_count.get) if tag_count else None

    print("\n--- STATS ---")
    print("Total contacts:", total)
    print("Most used tag:", most_used)
    print("Tags summary:", tag_count)

def menu():
    while True:
        print("\n 1. Add Contact\n 2. Search Contact \n 3. Update Contact \n 4. Delete Contact")
        print(" 5. Add Tag \n 6. Remove Tag \n 7. Find by Tag \n 8. Save Contacts \n 9. Load Contacts")
        print(" 10. Show Statistics \n0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            add_tag()
        elif choice == "6":
            remove_tag()
        elif choice == "7":
            find_by_tag()
        elif choice == "8":
            save_contacts()
        elif choice == "9":
            load_contacts()
        elif choice == "10":
            show_stats()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

menu()