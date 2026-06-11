# Shopping Cart System using Lists and List Methods

# Lists to store cart items
item_names = []
item_prices = []
item_quantities = []

def add_item(name, price, quantity):
    """
    Add a new item to the shopping cart.
    
    Parameters:
    name (str): The name of the item
    price (float): The price of the item
    quantity (int): The quantity to add
    """
    item_names.append(name)
    item_prices.append(price)
    item_quantities.append(quantity)
    print(f"Added '{name}' - Price: ${price}, Quantity: {quantity}")

def remove_item(item_index):
    """
    Remove an item from the shopping cart by index.
    
    Parameters:
    item_index (int): The index of the item to remove
    """
    if item_index >= 0 and item_index < len(item_names):
        removed_name = item_names.pop(item_index)
        item_prices.pop(item_index)
        item_quantities.pop(item_index)
        print(f"Removed '{removed_name}' from cart.")
    else:
        print("Invalid item index.")

def update_quantity(item_index, new_quantity):
    """
    Update the quantity of an item in the cart.
    
    Parameters:
    item_index (int): The index of the item
    new_quantity (int): The new quantity
    """
    if item_index >= 0 and item_index < len(item_names):
        old_quantity = item_quantities[item_index]
        item_quantities[item_index] = new_quantity
        print(f"Updated '{item_names[item_index]}' quantity from {old_quantity} to {new_quantity}")
    else:
        print("Invalid item index.")

def calculate_total():
    """
    Calculate the total price of all items in the cart.
    Apply 10% discount if total > $100.
    Returns the total price.
    """
    subtotal = 0.0
    
    for i in range(len(item_names)):
        item_total = item_prices[i] * item_quantities[i]
        subtotal = subtotal + item_total
    
    # Apply 10% discount if subtotal > $100
    if subtotal > 100:
        discount = subtotal * 0.10
        total = subtotal - discount
        return subtotal, discount, total
    else:
        return subtotal, 0, subtotal

def display_receipt():
    """
    Display an itemized receipt with all items, quantities, prices, and subtotals.
    """
    if len(item_names) == 0:
        print("Cart is empty. No receipt to display.")
        return
    
    print("\n" + "="*60)
    print("ITEMIZED RECEIPT")
    print("="*60)
    print(f"{'Item Name':<25} {'Qty':<5} {'Price':<12} {'Subtotal':<12}")
    print("-"*60)
    
    for i in range(len(item_names)):
        name = item_names[i]
        price = item_prices[i]
        quantity = item_quantities[i]
        subtotal = price * quantity
        print(f"{name:<25} {quantity:<5} ${price:<11.2f} ${subtotal:<11.2f}")
    
    print("-"*60)
    
    subtotal, discount, total = calculate_total()
    
    print(f"{'Subtotal:':<42} ${subtotal:.2f}")
    
    if discount > 0:
        print(f"{'Discount (10%):':<42} -${discount:.2f}")
    
    print(f"{'Total:':<42} ${total:.2f}") #:42 It makes the text left-aligned and takes 42 spaces width.
    print("="*60 + "\n") #print a separator line

def show_recently_added():
    """
    Display the last 3 items added to the cart using list slicing.
    """
    print("\nRecently Added Items (Last 3):")
    print("-"*50) #print a separator line
    
    if len(item_names) == 0:
        print("No items in cart.")
        return
    
    # Use slicing to get last 3 items
    last_three_names = item_names[-3:]
    last_three_prices = item_prices[-3:]
    last_three_quantities = item_quantities[-3:]
    
    for i in range(len(last_three_names)):
        name = last_three_names[i]
        price = last_three_prices[i]
        quantity = last_three_quantities[i]
        subtotal = price * quantity
        print(f"{name:<20} Qty: {quantity:<3} Price: ${price:<8.2f} Subtotal: ${subtotal:.2f}")
    
    print("-"*50 + "\n")

def display_cart(): #defines a function to display the current items in the cart
    """
    Display all items currently in the cart with their details.
    """
    if len(item_names) == 0:
        print("Cart is empty.")
        return
    
    print("\nCurrent Cart:")
    print("-"*60)
    for i in range(len(item_names)):
        print(f"{i}. {item_names[i]} - Price: ${item_prices[i]:.2f}, Qty: {item_quantities[i]}")
    print("-"*60 + "\n")


# Test the shopping cart system
add_item("Laptop", 799.99, 1)
add_item("Mouse", 25.50, 2)
add_item("Keyboard", 75.00, 1)
add_item("Monitor", 299.99, 1)
add_item("USB Cable", 9.99, 3)

# Display cart and receipt
display_cart()
display_receipt()
show_recently_added()

# Update quantity
update_quantity(1, 3)
display_receipt()

# Remove an item
remove_item(0)
display_cart()
display_receipt()

show_recently_added()
