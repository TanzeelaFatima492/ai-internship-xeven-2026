try:
    first_number = int(input("Enter First number: "))
    second_number = int(input("Enter Second number: "))

    print("Adding of", first_number, "and", second_number)
    print("Result:", first_number + second_number)

    print("Subtraction of", first_number, "and", second_number)
    print("Result:", first_number - second_number)

    print("Multiplication of", first_number, "and", second_number)
    print("Result:", first_number * second_number)

    print("Quotient of", first_number, "and", second_number)
    print("Result:", first_number / second_number)

except ValueError:
    print("Error: Please enter valid integers only (no text allowed).")

except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")