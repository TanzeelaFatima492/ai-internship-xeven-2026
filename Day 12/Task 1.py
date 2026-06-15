import math
def calculate_average(numbers, round_to=2):

    if not numbers:
        return "Error: List is empty"

    if not all(isinstance(n, (int, float)) for n in numbers):
        return "Error: Non-numeric value found"

    avg = sum(numbers) / len(numbers)
    return round(avg, round_to)

def find_median(numbers):

    if not numbers:
        return "Error: List is empty"

    if not all(isinstance(n, (int, float)) for n in numbers):
        return "Error: Non-numeric value found"

    numbers = sorted(numbers)
    n = len(numbers)
    mid = n // 2

    if n % 2 == 0:
        return (numbers[mid - 1] + numbers[mid]) / 2
    else:
        return numbers[mid]

def get_standard_deviation(numbers, round_to=2):

    if not numbers:
        return "Error: List is empty"

    if not all(isinstance(n, (int, float)) for n in numbers):
        return "Error: Non-numeric value found"

    mean = sum(numbers) / len(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    std_dev = math.sqrt(variance)

    return round(std_dev, round_to)


data = [10, 20, 30, 40, 50]

print("Average:", calculate_average(data))
print("Median:", find_median(data))
print("Standard Deviation:", get_standard_deviation(data))