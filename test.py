def factorial(num):
    if num == 1:
        return 1
    if num > 1:
        return factorial(num - 1) * num


print(factorial(5))
