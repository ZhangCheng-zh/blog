"""
Given an m x n grid of characters board and a string word, return true if word exists in the grid.
The word can be constructed from letters in sequentially adjacent cells, where "adjacent" cells are those horizontally, 
vertically, or diagonally neighboring.
The word must be formed by characters that all lie in a straight line. Once a starting cell and a direction are chosen, 
the path cannot change direction.

Constraints:

1 ≤ m, n ≤ 100
1 ≤ word.length ≤ 100
board and word consist of lowercase English letters.
"""
def wordSearch(board, word):
    if not board or not board[0]:
        return False
    
    numRows = len(board)
    numCols = len(board[0])
    wordLen = len(word)

    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for r in range(numRows):
        for c in range(numCols):
            if board[r][c] == word[0]:
                for dr, dc in DIRS:
                    found = True
                    for k in range(1, wordLen):
                        nr, nc = r + k * dr, c + k * dc

                        if not (0 <= nr < numRows and 0 <= nc < numCols and board[nr][nc] == word[k]):
                            found = False
                            break
                    
                    if found:
                        return True
    
    return False

def runTests():

    board1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f'],
        ['g', 'h', 'i'],
    ]
    assert wordSearch(board1, "abc") is True          # horizontal right
    assert wordSearch(board1, "cba") is True          # horizontal left
    assert wordSearch(board1, "adg") is True          # vertical down
    assert wordSearch(board1, "gda") is True          # vertical up
    assert wordSearch(board1, "aei") is True          # diagonal down-right
    assert wordSearch(board1, "iea") is True          # diagonal up-left
    assert wordSearch(board1, "ceg") is True          # diagonal down-left
    assert wordSearch(board1, "gec") is True          # diagonal up-right

    assert wordSearch(board1, "abe") is False         # not a straight line
    assert wordSearch(board1, "abf") is False         # would require direction change
    assert wordSearch(board1, "abcd") is False        # out of bounds

    board2 = [['a']]
    assert wordSearch(board2, "a") is True
    assert wordSearch(board2, "b") is False

    board3 = [
        ['a', 'a', 'a', 'a'],
        ['a', 'b', 'c', 'a'],
        ['a', 'd', 'e', 'a'],
        ['a', 'a', 'a', 'a'],
    ]
    assert wordSearch(board3, "abc") is True          # b->c is right, starts at (1,1)
    assert wordSearch(board3, "bde") is False         # not collinear
    assert wordSearch(board3, "ae") is True           # diagonal a(0,0)->e(2,2)

    print("All tests passed!")


runTests()

