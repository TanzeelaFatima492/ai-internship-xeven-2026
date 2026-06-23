products = {
    "1": {"name": "burger", "price": 210, "quantity": 1, "category": "fast food"},
    "2": {"name": "bread", "price": 100, "quantity": 1, "category": "breakfast"},
    "3": {"name": "pizza", "price": 350, "quantity": 2, "category": "fast food"},
    "4": {"name": "pencil", "price": 50, "quantity": 3, "category": "stationary"}
}

def add_product(name, price, quantity, category):
    product_id = str(len(products) + 1)
    products[product_id] = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "category": category
    }
    print("Product added!")

def update_stock(product_id, quantity):
    if product_id in products:
        products[product_id]["quantity"] = quantity
        print("Stock updated!")
    else:
        print("Product not found")

def search_by_category(category):
    found = False

    for pid, product in products.items():
        if product["category"].lower() == category.lower():
            print(pid, product)
            found = True

    if not found:
        print("No products found")


while True:
    print("\n*** Menu ***")
    print("\n1. View products")
    print("2. Add product")
    print("3. Search product")
    print("4. Update stock")
    print("0. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        print(products)

    elif choice == "2":
        name = input("Name: ")
        price = int(input("Price: "))
        quantity = int(input("Quantity: "))
        category = input("Category: ")

        add_product(name, price, quantity, category)

    elif choice == "3":
        category = input("Enter category: ")
        search_by_category(category)

    elif choice == "4":
        product_id = input("Product ID: ")
        quantity = int(input("New quantity: "))
        update_stock(product_id, quantity)

    elif choice == "0":
        print("Thanks for using!")
        break

    else:
        print("Invalid choice")