# add a list of student names and perform various operations on it
students_names = ["Ali", "Maryum", "Charlie", "Ahmed", "Eman"]
print("Printing the list of student names:")   
print(students_names)  #print the list of student names

students_names.append("Faris") #add a new student to the list
print("\nAfter adding a new student:")
print(students_names)

students_names.insert(2, "Qais") #insert a new student at index 2
print("\nAfter inserting a student at index 2:")
print(students_names)

students_names.remove("Eman") #remove a student by name
print("\nAfter removing a student:")
print(students_names)

students_names.pop(3) #remove a student by index (removing the student at index 3, which is "David")
print("\nAfter popping a student at index 3:")
print(students_names)

print("\nSlices of the student names list only showing 3 students:") #print the first three students in the list using slicing
print(students_names[0:3])

print("\nSorting list alphabetically:") #sort the list of student names in alphabetical order and print the sorted list
students_names.sort()
print(students_names)

