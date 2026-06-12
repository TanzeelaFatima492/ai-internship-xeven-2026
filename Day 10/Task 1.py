import json
import os

FILE_NAME = "students.json"

# Default data
students = {
    "Ali": {"grade": "A", "age": 20},
    "Bilal": {"grade": "B", "age": 22},
    "Sara": {"grade": "C", "age": 21}
}

# Load data
if os.path.exists(FILE_NAME): #os path check file exsist
    with open(FILE_NAME, "r") as file: #reading and after read close it 
        students = json.load(file) 

# Save data
def save_data():
    with open(FILE_NAME, "w") as file: #w wite mode
        json.dump(students, file, indent=4)

while True:

    print("Student System")
    print("1. View Students")
    print("2. Add Student")
    print("3. Update Grade")
    print("4. Find Top Student")
    print("5. Exit")

    choice = input("Enter choice: ")

    # View
    if choice == "1":

        for name, info in students.items():
            print(name, info["grade"],info["age"])

    # Add 
    elif choice == "2":

        name = input("Name: ")
        grade = input("Grade: ").upper()
        age = int(input("Age: "))

        students[name] = {
            "grade": grade,
            "age": age
        }

        save_data()
        print("Student Added!")

    # Update
    elif choice == "3":

        name = input("Student Name: ")

        if name in students:
            grade = input("New Grade: ").upper()
            students[name]["grade"] = grade
            save_data()
            print("Grade Updated!")
        else:
            print("Student Not Found!")

    # Top Student
    elif choice == "4":

        found = False

        for name, info in students.items():

            if info["grade"] == "A":
                print("Top Student:", name)
                found = True

        if not found:
            print("No A grade students.")

    # Exit
    elif choice == "5":

        print("Goodbye!")
        break

    else:
        print("Invalid Choice")