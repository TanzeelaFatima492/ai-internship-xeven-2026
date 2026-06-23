records = [f"Tanzeela {i}" for i in range(1, 1001)]  # 1000 records using list comphrension
marks = [f"Marks {i}" for i in range(1001,2001)]

for record in records:
    new_record = record.upper()   # Transformation
    print(new_record)

total = len(records)

for index, record in enumerate(records, start=1):
    print(f"Record {index} of {total}: {record}")

for record in records:

    if record == "":
        continue

    if record == "ERROR":
        print("Critical Error!")
        break

    print(record)

for name, mark in zip(records, marks):
    print(name, mark)