"""
Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:

'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).
The matching should cover the entire input string (not partial).

Example 1:

Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".
Example 2:

Input: s = "aa", p = "*"
Output: true
Explanation: '*' matches any sequence.
Example 3:

Input: s = "cb", p = "?a"
Output: false
Explanation: '?' matches 'c', but the second letter is 'a', which does not match 'b'.
"""

def wildcardMatch(s, p):
    m, n = len(s), len(p)
    # dp[i][j] mean if s[:i] and p[:j] is match
    # dp[0][0] is empty match empty
    dp = [[False for _ in range(n + 1)] for _ in range(m + 1)]

    # init condition
    dp[0][0] = True 

    for j in range(n):
        if p[j] == '*':
            dp[0][j + 1] = True
        else:
            break
    
    for i in range(m):
        for j in range(n):
            if p[j] == '*':
                dp[i + 1][j + 1] = dp[i + 1][j] | dp[i][j + 1]
            if p[j] == '?' or s[i] == p[j]:
                dp[i + 1][j + 1] = dp[i][j]
    # time O(mn) space O(mn)
    return dp[m][n]

assert wildcardMatch('aa', 'a') == False
assert wildcardMatch('aa', '*') == True
assert wildcardMatch('aa', '?a') == True
assert wildcardMatch('aa', '?b') == False
assert wildcardMatch('aa', '?*') == True