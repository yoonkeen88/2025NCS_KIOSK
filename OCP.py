import time
## oneToN
def oneToNLoop(n):
    """
    O(n) => linear time
    """
    s = time.time()
    result = 0
    for i in range(1,n+1):
        result += i
    e = time.time()
    print(f"Elapsed time: {e-s}")
    return result

def oneToNMath(n):
    """
    O(1) => constant time
    """
    s = time.time()
    result = n*(n+1)//2
    e = time.time()
    print(f"Elapsed time: {e-s}")    
    return result

i = int(input("Enter the number: "))

print(oneToNLoop(i) , "\n")
print(oneToNMath(i) , "\n")
