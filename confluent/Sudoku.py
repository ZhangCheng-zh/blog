"""
Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

Each row must contain the digits 1-9 without repetition.
Each column must contain the digits 1-9 without repetition.
Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.
Note:

A Sudoku board (partially filled) could be valid but is not necessarily solvable.
Only the filled cells need to be validated according to the mentioned rules.
 

Example 1:


Input: board = 
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true
Example 2:

Input: board = 
[["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: false
Explanation: Same as Example 1, except with the 5 in the top left corner being modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is invalid.
 

Constraints:

board.length == 9
board[i].length == 9
board[i][j] is a digit 1-9 or '.'.
"""
from typing import List

def isValidSudoku(board: List[List[str]]) -> bool:
    rows = [set() for i in range(9)]
    cols = [set() for i in range(9)]
    sub = [set() for i in range(9)]
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.': continue
            c = int(board[i][j])
            if c in rows[i] or c in cols[j] or c in sub[(i // 3) * 3 + j // 3]:
                return False
            else:
                rows[i].add(c)
                cols[j].add(c)
                sub[(i // 3) * 3 + j // 3].add(c)
    return True     


"""
Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:

Each of the digits 1-9 must occur exactly once in each row.
Each of the digits 1-9 must occur exactly once in each column.
Each of the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
The '.' character indicates empty cells.

 

Example 1:


Input: board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
Output: [["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]]
Explanation: The input board is shown above and the only valid solution is shown below:


Constraints:

board.length == 9
board[i].length == 9
board[i][j] is a digit or '.'.
It is guaranteed that the input board has only one solution.
"""
def solveSudoku(self, board: List[List[str]]) -> None:
    """
    Do not return anything, modify board in-place instead.
    """
    # first check the sudoku has answer
    # if not isValidSudoku(board): return False

    # record already used numbers for each row col and sub
    rows = [set() for i in range(9)]
    cols = [set() for i in range(9)]
    sub = [set() for i in range(9)]
    emptyCells = []

    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                emptyCells.append((i, j))
            else:
                c = int(board[i][j])
                rows[i].add(c)
                cols[j].add(c)
                sub[(i // 3) * 3 + j // 3].add(c)

    # dfs backtrack fill emptycells one by one
    def dfs(idx) -> bool:
        # filled all emptyCell with valid number
        # find answer
        if idx == len(emptyCells):
            return True

        i, j = emptyCells[idx]

        # try all candidates in target cell
        for x in range(1, 10):
            # x already used
            if x in rows[i] or x in cols[j] or x in sub[(i // 3) * 3 + j // 3]:
                continue
            
            board[i][j] = str(x)
            rows[i].add(x)
            cols[j].add(x)
            sub[(i // 3) * 3 + j // 3].add(x)

            if dfs(idx + 1):
                return True
            
            # restore
            rows[i].remove(x)
            cols[j].remove(x)
            sub[(i // 3) * 3 + j // 3].remove(x)

        return False
    
    dfs(0)