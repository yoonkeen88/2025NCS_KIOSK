import time

## timemeasure decorator
def timemeasure(func):
    def wrapper(*args, **kwargs): # 가변인자(많이 오면 많이 담고 아니면 아니고) inner function 
        s = time.time()
        result = func(*args, **kwargs)
        e = time.time()
        print(f"Elapsed time: {e-s}")
        return result
    return wrapper
# 클로저 문법이 쓰여진 decorator


## oneToN
def oneToNLoop(n):
    """
    O(n) => linear time
    """
    result = 0
    for i in range(1,n+1):
        result += i
    return result

@timemeasure
def oneToNMath(n):
    """
    O(1) => constant time
    """
    result = n*(n+1)//2
    return result

i = int(input("Enter the number: "))

print(oneToNLoop(i) , "\n")
print(oneToNMath(i) , "\n")

f = timemeasure(oneToNLoop)

print(f(i))