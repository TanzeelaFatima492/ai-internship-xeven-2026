import re
from datetime import datetime

def validate_email(email):

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not email:
        return False, "Email cannot be empty"

    if re.match(pattern, email):
        return True, "Valid email"
    else:
        return False, "Invalid email format"

def validate_phone(phone):

    pattern = r"^[0-9]{10,15}$"

    if not phone:
        return False, "Phone cannot be empty"

    if re.match(pattern, phone):
        return True, "Valid phone number"
    else:
        return False, "Phone must be 10–15 digits only"


def validate_date(date_str):

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, "Valid date"
    except ValueError:
        return False, "Invalid date format (use YYYY-MM-DD)"


def validate_password(password):


    if not password:
        return False, "Password cannot be empty"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain letters"

    if not re.search(r"[0-9]", password):
        return False, "Password must contain numbers"

    return True, "Strong password"


def validate_user_input(input_type, value):


    if input_type == "email":
        return validate_email(value)

    elif input_type == "phone":
        return validate_phone(value)

    elif input_type == "date":
        return validate_date(value)

    elif input_type == "password":
        return validate_password(value)

    else:
        return False, "Unknown input type"


if __name__ == "__main__":
    
    print(validate_user_input("email", "test@gmail.com"))
    print(validate_user_input("phone", "03001234567"))
    print(validate_user_input("date", "2026-06-15"))
    print(validate_user_input("password", "pass1234"))

    # Invalid examples
    print(validate_user_input("email", "wrong-email"))
    print(validate_user_input("password", "123"))