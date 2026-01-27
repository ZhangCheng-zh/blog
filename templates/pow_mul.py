# a @ b @ is matrix multiple
from typing import List

MOD = 10**9 + 7


# multiply two matrices with all entries taken modulo MOD
def mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [[sum(x*y for x, y in zip(row, col)) % MOD for col in zip(*b)] for row in a]



# a^n @ f1
# fast exponentiation of matrix `a` applied to `f1`, with all ops modulo MOD
def pow_mul(a: List[List[int]], n: int, f1: List[List[int]]) -> List[List[int]]:
    res = f1
    while n:
        if n & 1:
            res = mul(a, res)
        a = mul(a, a)
        n >>= 1
    return res
