messy_data = ["  Alice  ", "bob", None, "  CHARLIE  ", "alice", "  ", "David"]
print("Original data:", messy_data)

print("\nCleaned data:")
cleaned = []

for x in messy_data:
    if x is not None:              # remove None
        x = x.strip()              # remove spaces
        if x != "":                # remove empty strings
            cleaned.append(x.lower())
            print(x.lower())

print("\nRemove duplicates:")
final_data = []

for x in cleaned:
    if x not in final_data:
        final_data.append(x)
        print(x)

print("\nFinal cleaned data:", final_data)