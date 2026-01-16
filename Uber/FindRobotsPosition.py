"""
You are given a m * n board representing a position map and an array representing distances to the nearest blocker from a robot's position. The board is a 2D array where each cell can be:

'O': Represents a robot.
'E': Represents an empty space.
'X': Represents a blocker.
The boundary of the board is also considered a blocker. Additionally, you are provided with a distance array of four integers, which correspond to the distances to the closest blocker in the following order: left, top, bottom, and right.

Write a function that takes the position map and the distance array as inputs and returns the indices of all robots that match the given distance criteria.

Constraints:

The board dimensions are at least 1x1.
The distance array contains exactly four integers.
The matrix only contains 'O', 'E' and 'X'
"""
def findMatchingRobots(board, distance):
    m, n = len(board), len(board[0])
    targetLeft, targetTop, targetBottom, targetRight = distance

    leftDist = [[0] * n for _ in range(m)]
    rightDist = [[0] * n for _ in range(m)]
    topDist = [[0] * n for _ in range(m)]
    bottomDist = [[0] * n for _ in range(m)]


    for r in range(m):
        lastBlocker = -1
        for c in range(n):
            if board[r][c] == 'X':
                lastBlocker = c
            else:
                leftDist[r][c] = c - lastBlocker

        
        nextBlocker = n 
        for c in range(n - 1, -1, -1):
            if board[r][c] == 'X':
                nextBlocker = c
            else:
                rightDist[r][c] = nextBlocker - c
        
    for c in range(n):
        lastBlocker = -1
        for r in range(m):
            if board[r][c] == 'X':
                lastBlocker = r
            else:
                topDist[r][c] = r - lastBlocker
        
        nextBlocker = m
        for r in range(m - 1, -1, -1):
            if board[r][c] == 'X':
                nextBlocker = r
            else:
                bottomDist[r][c] = nextBlocker - r
    
    res = []
    for r in range(m):
        for c in range(n):
            if board[r][c] != 'O':
                continue
            if (leftDist[r][c] == targetLeft and
                topDist[r][c] == targetTop and
                bottomDist[r][c] == targetBottom and
                rightDist[r][c] == targetRight):
                res.append([r, c])
    
    return res

# Quick tests (from examples)
board1 = [
    ["O","E","E","E","X"],
    ["E","O","X","X","X"],
    ["E","E","E","E","E"],
    ["X","E","O","E","E"],
    ["X","E","X","E","X"]
]
assert findMatchingRobots(board1, [2,2,4,1]) == [[1,1]]

board2 = [
    ["O","E","X","O","O"],
    ["E","O","X","O","X"],
    ["X","X","O","E","E"],
    ["E","O","E","O","E"],
    ["O","O","X","O","O"]
]
assert findMatchingRobots(board2, [2,1,2,4]) == [[3,1]]

board3 = [
    ["O","X","O"],
    ["E","O","X"],
    ["O","X","O"]
]
# order depends on scan (row-major)
assert findMatchingRobots(board3, [1,1,1,1]) == [[0,2],[2,2]] or findMatchingRobots(board3, [1,1,1,1]) == [[2,2],[0,2]]
