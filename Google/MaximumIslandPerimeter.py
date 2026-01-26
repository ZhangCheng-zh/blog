"""
(This question is a variation of the LeetCode question 200. Number of Islands. If you haven't completed that question yet, it is recommended to solve it first.)

You are given a matrix grid of size m x n where each element is either land ('1') or water ('0'). A group of connected '1's (land) forms an island. Two land cells are considered connected if they are adjacent vertically or horizontally (not diagonally).

Each land cell has up to four edges. An edge contributes to the island's perimeter if it is either adjacent to water or lies on the boundary of the matrix.

Return the maximum perimeter among all islands in the grid. If there is no island, return 0.

Constraints:

1 ≤ m ≤ 100
1 ≤ n ≤ 100
Each grid[i][j] is either '0'(water) or '1'(land)
"""
# time O(m * n) space O(m * n)
def maxPerimeter(g):
    m, n = len(g), len(g[0])
    visited = [[0] * n for _ in range(m)]
    DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    # 
    def dfs(x, y):
        cnt = 0
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            # go grid outside
            if not (0 <= nx < m and 0 <= ny < n):
                cnt += 1
            # border of island
            elif g[nx][ny] == '0':
                cnt += 1
            elif visited[nx][ny] == 0:
                visited[nx][ny] = 1
                cnt += dfs(nx, ny)
        return cnt
    res = 0
    for x in range(m):
        for y in range(n):
            if visited[x][y] == 0 and g[x][y] == '1':
                visited[x][y] = 1
                cnt = dfs(x, y)
                res = max(res, cnt)
                
    return res

 # 1) No land
grid1 = [["0"]]
assert maxPerimeter(grid1) == 0

# 2) Single land cell
grid2 = [["1"]]
assert maxPerimeter(grid2) == 4

# 3) One island: 2x2 block -> perimeter 8
grid3 = [
    ["1", "1"],
    ["1", "1"],
]
assert maxPerimeter(grid3) == 8

# 4) Two separate single-cell islands -> max perimeter 4
grid4 = [
    ["1", "0", "1"],
]
assert maxPerimeter(grid4) == 4

# 5) L-shape island -> perimeter 8
# 1 1
# 1 0
grid5 = [
    ["1", "1"],
    ["1", "0"],
]
assert maxPerimeter(grid5) == 8

# 6) Two islands: (line of 3) perimeter 8, (single) perimeter 4 => max 8
grid6 = [
    ["1", "1", "1", "0"],
    ["0", "0", "0", "1"],
]
assert maxPerimeter(grid6) == 8

# 7) Complex: max should come from the big island
grid7 = [
    ["0","1","0","0","0"],
    ["1","1","1","0","0"],
    ["0","1","0","0","1"],
    ["0","0","0","1","1"],
]
# Island A is plus-shape-like (5 cells) perimeter = 12
# Island B is 3 cells connected (an L) perimeter = 8
assert maxPerimeter(grid7) == 12

print("All tests passed!")

# Uncomment to run locally:
# runTests()


