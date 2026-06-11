students_name = ["Ali", "Maryum", "Charlie", "Ahmed", "Eman"]
students_grades = ['A', 'B', 'A', 'C', 'B']

def grade_to_numeric(grade):
    """Convert letter grade to numeric value using list indexing"""
    grade_values = ['F', 'D', 'C', 'B', 'A']
    if grade in grade_values:
        return grade_values.index(grade)
    return 0

def add_student(name, grade):
    """
    Add a new student to the lists.
    
    Parameters:
    name (str): The name of the student
    grade (str): The grade of the student
    """
    students_name.append(name)
    students_grades.append(grade)
    print(f"Student '{name}' with grade '{grade}' has been added successfully!")

def remove_student(name):
    """
    Remove a student from the lists by name.
    
    Parameters:
    name (str): The name of the student to remove
    """
    if name in students_name:
        index = students_name.index(name)
        students_name.pop(index)
        students_grades.pop(index)
        print(f"Student '{name}' has been removed successfully!")
    else:
        print(f"Student '{name}' not found in the list.")

def update_grade(name, new_grade):
    """
    Update a student's grade.
    
    Parameters:
    name (str): The name of the student
    new_grade (str): The new grade for the student
    """
    if name in students_name:
        index = students_name.index(name)
        old_grade = students_grades[index]
        students_grades[index] = new_grade
        print(f"Student '{name}' grade has been updated from '{old_grade}' to '{new_grade}'!")
    else:
        print(f"Student '{name}' not found in the list.")

def get_average():
    """
    Calculate and display the average grade of all students.
    Converts letter grades to numeric values: A=4, B=3, C=2, D=1, F=0
    """
    total = 0
    
    for grade in students_grades:
        total = total + grade_to_numeric(grade)
    
    if len(students_grades) > 0:
        average = total / len(students_grades)
        print(f"Average grade (numeric): {average:.2f}") #format to 2 decimal places
    else:
        print("No students in the list.")

def find_highest_lowest_grades():
    """
    Find and display the highest and lowest grades with corresponding students.
    """
    if len(students_name) == 0:
        print("No students in the list.")
        return
    
    highest_student = students_name[0]
    highest_grade = students_grades[0]
    lowest_student = students_name[0]
    lowest_grade = students_grades[0]
    
    for i in range(len(students_name)):
        current_numeric = grade_to_numeric(students_grades[i])
        highest_numeric = grade_to_numeric(highest_grade)
        lowest_numeric = grade_to_numeric(lowest_grade)
        
        if current_numeric > highest_numeric:
            highest_student = students_name[i]
            highest_grade = students_grades[i]
        
        if current_numeric < lowest_numeric:
            lowest_student = students_name[i]
            lowest_grade = students_grades[i]
    
    print(f"Highest Grade: {highest_grade} - Student: {highest_student}")
    print(f"Lowest Grade: {lowest_grade} - Student: {lowest_student}")

def get_top_3_performers():
    """
    Sort students by grade (descending) and display top 3 performers.
    """
    if len(students_name) == 0:
        print("No students in the list.")
        return
    
    # Create list of indices sorted by numeric grade value (descending)
    sorted_indices = []
    for i in range(len(students_name)):
        sorted_indices.append(i) #indices= Track where each student is in the original list
    # Bubble sort in descending order
    for i in range(len(sorted_indices)):
        for j in range(len(sorted_indices) - 1 - i): #\
           # Compare numeric values of grades at sorted indices
           grade_to_numeric(students_grades[sorted_indices[j]]) 
            if grade_to_numeric(students_grades[sorted_indices[j]]) < grade_to_numeric(students_grades[sorted_indices[j + 1]]):
                temp = sorted_indices[j]
                sorted_indices[j] = sorted_indices[j + 1]
                sorted_indices[j + 1] = temp
    
    print("\nTop 3 Performers:")
    top_count = 3
    if len(sorted_indices) < 3:
        top_count = len(sorted_indices)
    
    for i in range(top_count):
        index = sorted_indices[i]
        name = students_name[index]
        grade = students_grades[index]
        numeric_value = grade_to_numeric(grade)
        print(f"{i + 1}. {name} - Grade: {grade} (Numeric: {numeric_value})")

def filter_students_by_average():
    """
    Use list methods to filter students above and below average.
    """
    if len(students_grades) == 0:
        print("No students in the list.")
        return
    
    # Calculate average
    numeric_grades = []
    for grade in students_grades:
        numeric_grades.append(grade_to_numeric(grade))
    
    total = 0
    for value in numeric_grades:
        total = total + value
    average = total / len(numeric_grades)
    
    # Filter using loops and append
    above_average = []
    below_average = []
    at_average = []
    
    for i in range(len(students_name)):
        if numeric_grades[i] > average:
            above_average.append(students_name[i])
        elif numeric_grades[i] < average:
            below_average.append(students_name[i])
        else:
            at_average.append(students_name[i])
    
    print(f"\nAverage Grade (numeric): {average:.2f}")
    print(f"\nAbove Average: {above_average}")
    print(f"Below Average: {below_average}")
    if len(at_average) > 0:
        print(f"At Average: {at_average}")



add_student("Sara", "A")
remove_student("Charlie")   
update_grade("Ahmed", "B")
get_average()
find_highest_lowest_grades()
get_top_3_performers()
filter_students_by_average()
