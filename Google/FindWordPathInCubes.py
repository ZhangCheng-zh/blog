""" 
You are given a word and a set of cubes. Each cube has 6 sides with a letter on each side. 
Spell the word using the cubes and return which cubes you used. Note: 
You cannot use the same cube to spell multiple letters. 
word = "phone" 
cubes = [ 
["h", "r", "y", "q", "t", "y"], 
["r", "m", "o", "f", "a", "r"], 
["r", "m", "p", "f", "a", "f"], 
["y", "z", "x", "n", "a", "b"], 
["g", "p", "z", "e", "m", "n"] 
] 
# Example output: [2, 0, 1, 3, 4]
"""
from collections import defaultdict

def spellWordWithCubes(word, cubes):
    m = len(word)
    n = len(cubes)
    # cube list become cube set help find letter
    cubeSets = [set(c) for c in cubes]

    # letter -> cubes
    wordToCube = defaultdict(list)
    for w in word:
        for idx, cs in enumerate(cubeSets):
            if w in cs:
                wordToCube[w].append(idx)
    
    print('wordToCube', wordToCube)
    
    visitedCube = [-1] * n
    ans = [-1] * m
    # iterate letter in word, find a valid choice for each letter
    def dfs(letterIdx):
        if letterIdx == m:
            return True

        letter = word[letterIdx]
        candidates = wordToCube[letter]

        for cubeIdx in candidates:
            if visitedCube[cubeIdx] != -1:
                continue

            visitedCube[cubeIdx] = 1
            ans[letterIdx] = cubeIdx

            if dfs(letterIdx + 1):
                return True

            visitedCube[cubeIdx] = -1
            ans[letterIdx] = -1
        
        return False
    
    ok = dfs(0)
    return ans if ok else []



# def spellWordWithCubes(word, cubes):
#     n = len(word)
#     m = len(cubes)

#     if n > m:
#         return []
    
#     cubeSets = [set(c) for c in cubes] # O(1) for search in cube

#     options = [] # options[i] means which cubes can supply word[i]
#     for ch in word:
#         candidates = [idx for idx in range(m) if ch in cubeSets[idx]]
#         options.append(candidates)

#     print('options:', options)
    
#     # order = sorted(range(n), key = lambda i: len(options[i]))

#     usedCubes = set()
#     assignment = [-1] * n

#     # first check smallest candidates
#     def backtrack(orderIdx):
#         # reach end condition, find a right choice
#         if orderIdx == n:
#             return True

#         # target letter position in word
#         pos = orderIdx

#         # choose candidate cube for target letter
#         for cubeIdx in options[pos]:
#             # skip already used cube
#             if cubeIdx in usedCubes:
#                 continue

#             # use a cube, add a pos info
#             usedCubes.add(cubeIdx)
#             assignment[pos] = cubeIdx

#             if backtrack(orderIdx + 1):
#                 return True
            
#             # restore the usedCube and pos info
#             usedCubes.remove(cubeIdx)
#             assignment[pos] = -1

#         return False
#     ok = backtrack(0)
#     # time O(m^n) space (n + m)
#     return assignment if ok else []
            
# --- quick test with your sample ---
word = "phone"
cubes = [
    ["h", "r", "y", "q", "t", "y"],  # 0
    ["r", "m", "o", "f", "a", "r"],  # 1
    ["r", "m", "p", "f", "a", "f"],  # 2
    ["y", "z", "x", "n", "a", "b"],  # 3
    ["g", "p", "z", "e", "m", "n"],  # 4
]

print(spellWordWithCubes(word, cubes))  # one valid output: [2, 0, 1, 3, 4]
