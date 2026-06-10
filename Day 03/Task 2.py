#Taking number from users

grade=(int(input("Enter your grade: ")))

# add logic to check the grade and print the appropriate message
#use try-except block to handle non-numeric input and invalid grade values
try:
    if grade < 0 or grade > 100:
        print("Invalid grade entered. Grade must be between 0 and 100.")
    elif grade >= 90:
        print("Your grade is A. Good work !")
    elif grade >= 80:
        print("Your grade is B. Keep it up!")
    elif grade >= 70:
        print("Your grade is C. You can do better!")
    elif grade >= 60:
        print("Your grade is D. Keep working hard!")
    else:
        print("Your grade is F. Don't give up!")

# Handle non-numeric input        
except ValueError:
    print("Please enter a valid numeric grade.")