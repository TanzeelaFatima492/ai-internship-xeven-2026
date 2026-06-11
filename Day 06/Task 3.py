num_list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
print("Original list of numbers:") # print the original list of numbers
print(num_list)

print("first 5 numbers:")
print(num_list[0:5]) # print the first 5 numbers in the list using slicing

print("\nlast 5 numbers:")
print(num_list[-5:]) # print the last 5 numbers in the list using slicing

print("\nEvery 3rd number:")
print(num_list[::3]) # print every 3rd number in the list using slicing

print("\nReversed list of numbers:")
print(num_list[::-1]) # print the list of numbers in reverse order using slicing

print("\nMid 10 numbers:")
print(num_list[5:15]) # print the middle 10 numbers in the list using slicing