words = ["  hello ", " world ", " python "]
print(words)
result = list(map(lambda x: x.strip().upper(), words))
print(result)

data = [
    "user@gmail.com",
    "call me 03001234567",
    "https://google.com",
    "random text"
]

emails = list(filter(lambda x: "@" in x, data))
phones = list(filter(lambda x: x.replace(" ", "").isdigit() or "03" in x, data))
urls = list(filter(lambda x: "http" in x, data))

print("Emails:", emails)
print("Phones:", phones)
print("URLs:", urls)

students = [
    {"name": "Ali", "age": 20},
    {"name": "Sara", "age": 18},
    {"name": "Ali", "age": 18}
]

result = sorted(students, key=lambda x: (x["name"], x["age"]))
print(result)