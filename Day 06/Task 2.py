students_names = ["Ali", "Maryum", "Charlie", "Ahmed", "Eman"]
students_marks = [85, 92, 78, 100, 88]

highest_grade = max(students_marks)
highest_grade_index = students_marks.index(highest_grade)
highest_student_name = students_names[highest_grade_index]

print(f"\nHighest Grade: {highest_grade}")
print(f"Student Name: {highest_student_name}")

lowest_grade = min(students_marks)
lowest_grade_index = students_marks.index(lowest_grade) 
lowest_student_name = students_names[lowest_grade_index]

print(f"\nLowest Grade: {lowest_grade}")
print(f"Student Name: {lowest_student_name}")

average_grade = sum(students_marks) / len(students_marks)
print(f"\nAverage Grade: {average_grade:.2f}")

if lowest_grade >= 60:
    print("All students passed the exam.")
else:
    print("Some students failed the exam.")