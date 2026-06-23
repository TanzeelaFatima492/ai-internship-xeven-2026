import math # Importing the math module to perform mathematical operations

cities = (
    ("Islamabad", 33.6844, 73.0479),
    ("Lahore", 31.5204, 74.3587),
    ("Karachi", 24.8607, 67.0011),
    ("Peshawar", 34.0151, 71.5249),
    ("Quetta", 30.1798, 66.9750),
    ("Multan", 30.1575, 71.5249),
    ("Faisalabad", 31.4504, 73.1350)
)

print("Cities and their coordinates:")
print(cities)

def calculate_distance(coord1, coord2):
    lat1, lon1 = coord1  # Latitude and Longitude of the first coordinate
    lat2, lon2 = coord2

    return math.sqrt(
        (lat2 - lat1)**2 + # Latitude difference squared
        (lon2 - lon1)**2 # Longitude difference squared
    )

def closest_city(location):
    nearest = None
    minimum = float("inf")

    for city in cities:
        name, lat, lon = city

        d = calculate_distance(
            location,
            (lat, lon) # Calculate the distance between the user's location and the city's coordinates
        )

        if d < minimum:
            minimum = d
            nearest = name

    return nearest, minimum


user_location = (32.5, 74.0)
print("your Location:", user_location)

city, distance = closest_city(user_location)

print("Nearest City:", city)
print("Distance:", round(distance, 2))
