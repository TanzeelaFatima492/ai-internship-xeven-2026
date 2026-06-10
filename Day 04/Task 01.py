username = input("Enter your username(5): ")
password = input("Enter your password(8): ")
age = int(input("Enter your age(18+): "))

if age > 18 and len(username) >= 5 and len(password) >= 8:
    print("You are granyeted access to create an account.")
else:
    print("check your username, password, and age requirements.")