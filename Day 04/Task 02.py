number_one=float(input("Enter the first number: "))
number_two=float(input("Enter the second number: "))
operation=input("Enter the operation (+, -, *, /, %, **): ")

try:
    if number_two == 0:
        print("Error: Division by zero is not allowed.")
    elif operation == "+":
       print(f"Result od addition: {number_one + number_two}")
    elif operation == "-":
        print(f"Result of subtraction: {number_one - number_two}")
    elif operation == "*":
        print(f"Result of multiplication: {number_one * number_two}")
    elif operation == "/":
        print(f"Result of division : {number_one / number_two}")
    elif operation == "%":
        print(f"Result of modulus: {number_one % number_two}")
    elif operation == "**":
        print(f"Result of exponentiation: {number_one ** number_two}")
    else:
        print("Error: Invalid operation.")
except ValueError:
    print("Error: Please enter valid numbers.")