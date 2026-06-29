import psycopg2

#    DATABASE CONNECTION   
conn = psycopg2.connect(
    host="localhost",
    database="chatbot_db",
    user="postgres",
    password="12345",
    port="5432"
)

cur = conn.cursor()

#    CREATE TABLE   
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    department VARCHAR(100)
)
""")
conn.commit()

#    MENU   
while True:
    print("\nSTUDENT MANAGEMENT")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter your choice: ")

    #      CREATE     
    if choice == "1":
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        department = input("Enter Department: ")

        cur.execute(
            "INSERT INTO students(name, age, department) VALUES (%s, %s, %s)",
            (name, age, department)
        )
        conn.commit()
        print(" Student Added Successfully!")

    #      READ     
    elif choice == "2":
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()

        if not rows:
            print("No students found.")
        else:
            print("\nID\tName\t\tAge\tDepartment")
            print("-" * 45)
            for row in rows:
                print(f"{row[0]}\t{row[1]}\t\t{row[2]}\t{row[3]}")

    #      UPDATE     
    elif choice == "3":
        student_id = int(input("Enter Student ID to Update: "))
        name = input("Enter New Name: ")
        age = int(input("Enter New Age: "))
        department = input("Enter New Department: ")

        cur.execute(
            """
            UPDATE students
            SET name=%s, age=%s, department=%s
            WHERE id=%s
            """,
            (name, age, department, student_id)
        )
        conn.commit()

        if cur.rowcount > 0:
            print(" Student Updated Successfully!")
        else:
            print(" Student ID not found.")

    #      DELETE     
    elif choice == "4":
        student_id = int(input("Enter Student ID to Delete: "))

        cur.execute(
            "DELETE FROM students WHERE id=%s",
            (student_id,)
        )
        conn.commit()

        if cur.rowcount > 0:
            print(" Student Deleted Successfully!")
        else:
            print(" Student ID not found.")

    #      EXIT     
    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid Choice! Please try again.")

cur.close()
conn.close()