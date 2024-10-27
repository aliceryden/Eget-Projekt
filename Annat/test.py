import math

print("select an operation: ")
print("1. ADD")
print("2. SUB")
print("3. MULU")
print("4. DIV")

operation = input()

digit1 = float(input("Enter a digit: "))
digit2 = float(input("Enter another digit: "))


if operation == "1":
    result = digit1 + digit2
    print(f"The sum is: {result}")
elif operation == "2":
    result = digit1 - digit2
    print(f"The diffrence is: {result}")
elif operation == "3":
    result = digit1 * digit2
    print(f"The prouct is: {result}")
elif operation == "4":
    if digit2 != 0:
        result = digit1 / digit2
        print(f"The sum is: {result}")
    else:
        print("Error, division by zero is not possible. ")
else:
    print("Invalid entry. ")



