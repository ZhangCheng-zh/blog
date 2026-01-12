"""
Given an input string s and a pattern p, implement wildcard matching with these rules:
p contains only lowercase/uppercase letters and optionally one *.
There is no ? in the pattern.
* (if present) matches any sequence of characters, including the empty sequence.
The match must cover the entire string s (not partial).
Return True if p matches s, otherwise False.

Examples
s="aa", p="a" → False
s="aa", p="*" → True
s="abcd", p="ab*cd" → True
s="abcd", p="ab*ce" → False
s="abcd", p="*cd" → True
s="abcd", p="ab*" → True
"""
# p has zero or one '*'
def matchStr(s, p):
    if '*' not in p:
        return s == p
    
    left, right = p.split('*')
    if len(s) < len(left) + len(right):
        return False 
    
    return s.startswith(left) and s.endswith(right)

assert matchStr("","") == True
assert matchStr("","a") == False
assert matchStr("aa","") == False
assert matchStr("aa","a") == False
assert matchStr("aa","*") == True
assert matchStr("abcd", "ab*cd") == True
assert matchStr("abcd","ab*ce") == False
assert matchStr("abcd","*cd") == True
assert matchStr("abcd", "ab*") == True
assert matchStr("a", "a*a") == False


"""
You are given an input string s and a pattern p.
p contains letters and zero, one, or many * characters.
There is no ?.
* matches any sequence of characters, including empty.
Matching must cover the entire string s.
Implement is_match(s, p) -> bool.

Examples
s="aa", p="*" → True
s="abcd", p="a*d" → True
s="abcd", p="a**c*d" → True (treat consecutive * like one)
s="abcd", p="a*c" → False
s="", p="**" → True
"""
# p has 0 - n '*' 
def matchStr2(s, p):
    if '*' not in p:
        return s == p 

    parts = p.split('*')
    parts = [p for p in parts if p != '']

    startWithStar = p[0] == '*'
    endWithStar = p[-1] == '*'

    # use two pointer match s and p
    i = 0

    if not startWithStar and parts:
        if not s.startswith(parts[0]):
            return False
        i = len(parts[0])
        parts = parts[1:]

    last = None
    if not endWithStar and parts:
        last = parts[-1]
        parts = parts[:-1]
    
    
    # match all middle part
    for p in parts:
        tmp = s.find(p, i)
        if tmp == -1:
            return False
        i = tmp + len(p)
    
    # if exist tail, need match
    if last:
        lastStartIndex = len(s) - len(last)
        
        # tail of s is shorter than tail of p
        if i > lastStartIndex:
            return False
        
        return s.endswith(last)
    return True
        
    
    

# Empty / exact cases
assert matchStr2("", "") == True
assert matchStr2("", "a") == False
assert matchStr2("", "*") == True
assert matchStr2("", "**") == True
assert matchStr2("aa", "") == False
assert matchStr2("aa", "aa") == True
assert matchStr2("aa", "a") == False

# Single '*'
assert matchStr2("aa", "*") == True
assert matchStr2("aa", "a*") == True
assert matchStr2("aa", "*a") == True
assert matchStr2("ab", "a*b") == True          # '*' empty
assert matchStr2("abcd", "ab*cd") == True
assert matchStr2("abcd", "ab*ce") == False
assert matchStr2("abcd", "*cd") == True
assert matchStr2("abcd", "*ce") == False
assert matchStr2("abcd", "ab*") == True
assert matchStr2("abcd", "ac*") == False
assert matchStr2("a", "a*a") == False          # important length corner
assert matchStr2("aba", "a*a") == True
assert matchStr2("ab", "a*a") == False

# Many '*' (including consecutive)
assert matchStr2("abcd", "**") == True
assert matchStr2("abcd", "a**d") == True
assert matchStr2("abcd", "a***d") == True
assert matchStr2("abcd", "***ab***cd***") == True
assert matchStr2("abcd", "***ab***ce***") == False

# Ordered chunks with multiple '*'
assert matchStr2("abcd", "a*b*c*d") == True
assert matchStr2("abcd", "a*b*d") == True
assert matchStr2("abcd", "a*d*c") == False     # wrong order
assert matchStr2("abcd", "*a*b*c*d*") == True
assert matchStr2("abcd", "*a*c*b*") == False   # wrong order

# Prefix/suffix anchoring
assert matchStr2("zzzabc", "abc*") == False
assert matchStr2("abczzz", "abc*") == True
assert matchStr2("zzzabc", "*abc") == True
assert matchStr2("zzzabczzz", "*abc") == False

# Overlap / tight length
assert matchStr2("aaaaa", "aa*aa") == True
assert matchStr2("aaa", "aa*aa") == False
assert matchStr2("ababa", "ab*aba") == True
assert matchStr2("ababa", "aba*aba") == False

# Middle contains
assert matchStr2("abc", "*b*") == True
assert matchStr2("ac", "*b*") == False
assert matchStr2("abc", "**b**") == True

# Case sensitivity
assert matchStr2("Abc", "A*") == True
assert matchStr2("Abc", "a*") == False
