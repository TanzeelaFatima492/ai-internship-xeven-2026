valid_domains = {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "zoho.com"}

registered_emails = set()

def validate_email(email):
    email = email.lower()

    if "@" not in email:
        return False

    parts = email.split("@")
    if len(parts) != 2:
        return False

    local, domain = parts

    if local == "":
        return False

    return domain in valid_domains


def register_email(email):
    email = email.lower()

    if not validate_email(email):
        print("Invalid email")
        return

    if email in registered_emails:
        print("Already registered")
        return

    registered_emails.add(email)
    print("Registered")


print("Email Validation System")

while True:
    email = input("Enter email (or type stop): ")

    if email.lower() == "stop":
        break

    register_email(email)


print("\nFinal Emails:", registered_emails)
print("Total:", len(registered_emails))