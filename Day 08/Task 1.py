students_name = ["Ali", "Maryum", "Charlie", "Ahmed", "Eman"]
students_grades = ['A', 'B', 'A', 'C', 'B']

grade conversion
def grade_value(grade):
    if grade == 'A':
        return 4
    elif grade == 'B':
        return 3
    elif grade == 'C':
        return 2
    elif grade == 'D':
        return 1
    else:
        return 0


def add_student(name, grade):
    students_name.append(name)
    students_grades.append(grade)
    print(name, "added")


def remove_student(name):
    if name in students_name:
        i = students_name.index(name)
        students_name.pop(i)
        students_grades.pop(i)
        print(name, "removed")
    else:
        print("Not found")


def update_grade(name, grade):
    if name in students_name:
        i = students_name.index(name)
        students_grades[i] = grade
        print(name, "updated")
    else:
        print("Not found")


def get_average():
    total = 0
    for g in students_grades:
        total += grade_value(g)

    avg = total / len(students_grades)
    print("Average:", round(avg, 2))


def show_best_and_worst():
    best_i = 0
    worst_i = 0

    for i in range(len(students_grades)):
        if grade_value(students_grades[i]) > grade_value(students_grades[best_i]):
            best_i = i
        if grade_value(students_grades[i]) < grade_value(students_grades[worst_i]):
            worst_i = i

    print("Highest:", students_name[best_i], students_grades[best_i])
    print("Lowest:", students_name[worst_i], students_grades[worst_i])


def show_top_3():
    data = list(zip(students_name, students_grades))

    # simple sort using grade value
    data.sort(key=lambda x: grade_value(x[1]), reverse=True)

    print("Top 3 Students:")
    for i in range(min(3, len(data))):
        print(i + 1, data[i][0], "-", data[i][1])


add_student("Sara", "A")
remove_student("Charlie")
update_grade("Ahmed", "B")

get_average()
show_best_and_worst()
show_top_3()