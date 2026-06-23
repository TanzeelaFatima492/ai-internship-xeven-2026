# Multiplication table from 1 to 5

for i in range(1, 6):          # outer loop
    for j in range(1, 6):      # inner loop
        print(i * j, end="\t")
    print()  # new line after each row

rows = 5

for i in range(1, rows + 1):
    for j in range(rows - i):
        print(" ", end="")

    for k in range(2 * i - 1):
        print("*", end="")

    print()

rows = 5

for i in range(1, rows + 1):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for i in range(3):
    for j in range(3):
        print(matrix[j][i], end=" ")
    print()


for row in matrix:
    print("sum of rows")
    print(sum(row))

for col in range(3):
    total = 0
    for row in range(3):
        total += matrix[row][col]
    print("Sum of columns :")
    print(total)

# Main diagonal
for i in range(3):
    print(matrix[i][i])

rows = 5
cols = 10

for i in range(rows):
    for j in range(cols):
        print("*", end="")
    print()

rows = 5
cols = 10

for i in range(rows):
    for j in range(cols):
        if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
            print("*", end="")
        else:
            print(" ", end="")
    print()