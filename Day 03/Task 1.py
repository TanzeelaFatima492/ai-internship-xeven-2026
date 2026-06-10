# Ask the user for their name
user_name = input("What is your name? ")

# Welcome message
print(f"Hello, {user_name}! Welcome to the world of programming!")

try:
    # Ask the user for their age and convert it to an integer
    user_age = int(input("How old are you? "))

    # Display the entered age
    print(f"Your age is {user_age}")

    # Check for invalid age
    if user_age < 0:
        print("Invalid age entered. Age cannot be negative.")

    # Child category
    elif user_age < 13:
        print(f"Hello {user_name}! You are a child. Enjoy your childhood and keep learning new things!")

    # Teenager category
    elif user_age <= 17:
        print(f"Hello {user_name}! As a teenager, you have many opportunities ahead.")

    # Adult category
    elif user_age <= 64:
        print(f"Hello {user_name}! Welcome to the world of programming!")

    # Senior category
    else:
        print(f"Hello {user_name}! It's never too late to learn something new!")

# Handle non-numeric input
except ValueError:
    print("Please enter a valid numeric age.")