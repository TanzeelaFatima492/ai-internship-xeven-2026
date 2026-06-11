# Shopping Cart System using Lists and List Methods

# Lists to store cart items
names = []
prices = []
qtys = []

def add(name, price, qty):
    names.append(name)
    prices.append(price)
    qtys.append(qty)
    print("Added:", name)


def remove(index):
    if index < len(names):
        print("Removed:", names[index])
        names.pop(index)
        prices.pop(index)
        qtys.pop(index)
    else:
        print("Invalid index")


def update(index, new_qty):
    if index < len(names):
        qtys[index] = new_qty
        print("Updated:", names[index])

def total():
    t = 0

    for i in range(len(names)):
        t += prices[i] * qtys[i]

    return t


def show():
    print("\nCart Items:")

    for i in range(len(names)):
        print(i, names[i], prices[i], qtys[i])


def receipt():
    print("\n----- RECEIPT -----")

    for i in range(len(names)):
        sub = prices[i] * qtys[i]
        print(names[i], "x", qtys[i], "=", sub)

    print("Total:", total())

print("adding items to cart...")
add("Laptop", 800, 1)
add("Mouse", 25, 2)
add("Keyboard", 75, 1)


show()
receipt()

print("\nUpdating quantity of Mouse to 3...")
update(1, 3)
receipt()

print("\nRemoving laptop from cart...")
remove(0)
show()
receipt()