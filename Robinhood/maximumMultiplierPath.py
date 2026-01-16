"""
Maximum Multiplier Path
You are given a directed graph with n nodes labeled 0 .. n-1.
Each directed edge is [u, v, w], meaning you can go from u to v and multiply your current value by w.
You are also given two nodes: start and end.

Task
Find the maximum product of multipliers along any simple path from start to end.
A simple path means you cannot visit the same node more than once.
If no simple path exists from start to end, return -1.

Input
n: int
edges: List[List[int]] where each edge is [u, v, w]
start: int
end: int

Output
int: the maximum product, or -1 if impossible

Constraints
1 <= w <= 1e5
0 <= start, end < n
The graph may contain cycles, but your chosen path must be simple.
"""
# from collections import defaultdict
# import heapq

from typing import List, Tuple

def maxMultiplierProduct(self, n: int, edges: List[List[int]], start: int, end: int) -> int:
    g = [[] for _ in range(n)]

    for u, v, w in edges:
        g[u].append((v, w))
    
    # simple path rule: no node can be visited twice
    visited = set()

    def dfs(u):
        if u == end:
            return 1
        visited.add(u)
        best = -1

        for v, w in g[u]:
            if v in visited:
                continue
            sub = dfs(v)
            if sub != -1: # has a valid path
                best = max(best, w * sub)
        
        visited.remove(u) # restore the path
        return best
    
    return dfs(start)



# T1: Example 1 (best path is 0->1->2->4->3)
n = 5
edges = [[0, 1, 2], [1, 2, 3], [2, 1, 4], [1, 3, 5], [2, 4, 6], [4, 3, 10]]
start, end = 0, 3
expected = 360
assert maxMultiplierProduct(n, edges, start, end) == expected


# T2: Example 2 (cycle exists, but best simple path is 0->1->3)
n = 4
edges = [[0, 1, 1], [1, 2, 2], [2, 1, 3], [1, 3, 4]]
start, end = 0, 3
expected = 4
assert maxMultiplierProduct(n, edges, start, end) == expected


# T3: Example 3 (end is unreachable from start)
n = 6
edges = [[0, 1, 2], [1, 2, 3], [2, 0, 4], [3, 4, 5], [4, 5, 6]]
start, end = 0, 3
expected = -1
assert maxMultiplierProduct(n, edges, start, end) == expected


# T4: Start equals end (empty path is allowed -> product = 1)
n = 3
edges = [[0, 1, 5], [1, 2, 7]]
start, end = 1, 1
expected = 1
assert maxMultiplierProduct(n, edges, start, end) == expected


# T5: Multiple paths exist, choose the maximum product
# 0->1->3 = 2*3=6
# 0->2->3 = 10*1=10 (best)
n = 4
edges = [[0, 1, 2], [1, 3, 3], [0, 2, 10], [2, 3, 1]]
start, end = 0, 3
expected = 10
assert maxMultiplierProduct(n, edges, start, end) == expected


# T6: Critical case: a "gain cycle" (product > 1) exists.
# The problem requires a SIMPLE path (no repeated nodes), so the answer is finite.
# Best simple path: 0->1->2->3 = 2*2*2 = 8
# If cycles were allowed, the product could grow without bound.
n = 4
edges = [[0, 1, 2], [1, 2, 2], [2, 1, 2], [2, 3, 2]]
start, end = 0, 3
expected = 8
assert maxMultiplierProduct(n, edges, start, end) == expected
