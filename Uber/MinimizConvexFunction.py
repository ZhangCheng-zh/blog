"""
You are given access to a black-box function, F(x), which is convex over a given closed interval [a, b]. 
You can only interact with this function by calling a provided evaluate(x) function, which returns the value of F(x).
Your task is to find a point x* within the interval [a, b] that is within a specified precision, eps, 
of the true location of the minimum. In other words, if x_min is the point where the function's minimum occurs, 
find an x* such that |x* - x_min| ≤ eps.
Hint: A key property of a convex function on an interval is that it is unimodal, meaning it has a single minimum. 
This property allows for efficient search algorithms.
"""
import math
class ConvexFunction:
    def __init__(self, func):
        self.func = func
    
    def evaluate(self, x):
        return self.func(x)
    
class Solution:
    def __init__(self, func):
        self.func = func
    
    def minimize(self, a, b, eps):
        while (b - a) > eps:
            m1 = a + (b - a) / 3
            m2 = b - (b - a) / 3

            f1 = self.func.evaluate(m1)
            f2 = self.func.evaluate(m2)

            if f1 < f2:
                b = m2
            else:
                a = m1
        return (a + b) / 2

def test1():
    print("===== Test 1 =====")
    func = ConvexFunction(lambda x: (x - 3)**2 + 5)
    solution = Solution(func)
    result = solution.minimize(-10, 10, 0.01)
    print(f"Result: {result}")  # Expected: ~3.0

def test2():
    print("===== Test 2 =====")
    func = ConvexFunction(lambda x: x**2)
    solution = Solution(func)
    result = solution.minimize(-100, 50, 0.001)
    print(f"Result: {result}")  # Expected: ~0.0

def test3():
    print("===== Test 3 =====")
    func = ConvexFunction(lambda x: abs(x - 123.456))
    solution = Solution(func)
    result = solution.minimize(0, 1000, 0.0001)
    print(f"Result: {result}")  # Expected: ~123.456

def test4():
    print("===== Test 4 =====")
    func = ConvexFunction(lambda x: (x - 987.654)**2)
    solution = Solution(func)
    result = solution.minimize(-1e9, 1e9, 1e-4)
    print(f"Result: {result}")  # Expected: ~987.654

def test5():
    print("===== Test 5 =====")
    func = ConvexFunction(lambda x: math.exp(x) - 2 * x)
    solution = Solution(func)
    result = solution.minimize(0, 2, 1e-4)
    print(f"Result: {result}")  # Expected: ~0.693

def test6():
    print("===== Test 6 =====")
    func = ConvexFunction(lambda x: x)
    solution = Solution(func)
    result = solution.minimize(0, 100, 1e-4)
    print(f"Result: {result}")  # Expected: ~0.0

def test7():
    print("===== Test 7 =====")
    func = ConvexFunction(lambda x: (x - 1)**2)
    solution = Solution(func)
    result = solution.minimize(0.9999, 1.0001, 1e-4)
    print(f"Result: {result}")  # Expected: ~1.0

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()