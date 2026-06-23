n = 50

num = 2

print("Prime numbers up to", n, "are:")

while num <= n:
    is_prime = True
    i = 2

    while i * i <= num:   # optimization: i <= sqrt(num)
        if num % i == 0:
            is_prime = False
            break
        i += 1

    if is_prime:
        print(num, end=" ")

    num += 1


n = 10

a = 0
b = 1
count = 0

print("\nFibonacci sequence:")

while count < n:
    print(a, end=" ")

    temp = a + b
    a = b
    b = temp

    count += 1

n = 5
fact = 1
i = 1

while i <= n:
    fact *= i
    i += 1

print("\nFactorial of", n, "is:", fact)


secret = 7
attempts = 5

while attempts > 0:
    guess = int(input("Guess the number (1-10): "))

    if guess == secret:
        print("🎉 Correct! You win!")
        break

    elif guess > secret:
        print("Hint: Too high")

    else:
        print("Hint: Too low")

    attempts -= 1
    print("Attempts left:", attempts)

else:
    print("❌ Game Over! The number was:", secret)