def calculate(operation,x,y):
    if operation == 'Addition':
        return x + y
    elif operation == 'Substraction':
        if x>y:
            return x-y
        else :
            return y-x
    elif operation == 'Multiplication':
        return x*y

    else :
        return 'test'
