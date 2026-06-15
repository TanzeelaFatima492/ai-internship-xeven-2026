nested = [[1, 2], [3, 4], [5, 6]]

flat = [item for sublist in nested for item in sublist]
print(flat)

matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

transpose = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
print(transpose)

data = {"a": 1, "b": 2, "c": 3}

inverse = {v: k for k, v in data.items()}
print(inverse)

data = {"a": 1, "b": 2, "c": 3}

inverse = {v: k for k, v in data.items()}
print(inverse)