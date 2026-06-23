age = input("What is your age? ")
income= input("What is your income? ")
credit_score = input("What is your credit score? ")

try :
    if int(age) < 18:
        print("You are not eligible for a loan1.")
    else:
        if int(income) > 30000:
            print("You are not eligible for a loan2.")
        else:
            if int(credit_score) < 600:
                print("You are not eligible for a loan.")
            else:
                print("You are eligible for a loan.")

except ValueError:
    print("Please enter valid numbers for age, income, and credit score.")