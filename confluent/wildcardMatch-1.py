"""
Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:

'.' Matches any single character.​​
'*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial).


Example 1:
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".

Example 2:
Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".

Example 3:
Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.)".
"""

def wildcardMatch(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    # init condition
    dp[0][0] = True
    
    for j in range(1, n, 2):
        if p[j] != '*':
            break
        dp[0][j + 1] = True
    
    for i in range(m):
        for j in range(n):
            if p[j] == '*': 
                dp[i + 1][j + 1] = dp[i + 1][j - 1] | ((p[j - 1] == s[i] or p[j - 1] == '.') and dp[i][j + 1])
            else:
                (p[j] == s[j] or p[j] == '.') and dp[i + 1][j + 1] == dp[i][j]
    
    return dp[-1][-1]

assert wildcardMatch('aa', 'a') == False
assert wildcardMatch('aa', 'a*') == True
assert wildcardMatch('ab', '.*') == True