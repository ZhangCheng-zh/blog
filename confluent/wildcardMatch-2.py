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
    
    index = p.find('*')
    prefix = p[:index]
    suffix = p[index + 1:]

    if len(s) < len(prefix) + len(suffix):
        return False

    # s should have same prefix and same suffix
    if s.startswith(prefix) and s.endswith(suffix):
        return True 
    return False

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
    parts = [seg for seg in parts if seg]

    startWithStar = p[0] == '*'
    endWithStar = p[-1] == '*'

    i = 0
    # use pointer scan s, if match each part of p
    
    # if p not start with '*', head of s should match parts[0]
    if not startWithStar and parts:
        if not s.startswith(parts[0]): 
            return False
        i = len(parts[0]) # next start position of pointer
        parts = parts[1:] # update left parts
        
    # if p not end with '*', end of s should match parts[-1]
    last = None
    if not endWithStar and parts:
        last = parts[-1] # save end of p temperally
        parts = parts[:-1]
    
    # try match middle parts
    for part in parts:
        pos = s.find(part, i)
        if pos == -1: # not find next match
            return False
        i = pos + len(part) # update next start pointer
    
    # check last if match
    # s must end with last and head index of not scanned s should be smaller than head index of last
    if last is not None:
        lastStartIndex = len(s) - len(last)
        if i > lastStartIndex:
            return False
        return s.endswith(last)

    return True


def matchStr2(s, p):
    if '*' not in p:
        return s == p
    
    startWithStar = p[0] == '*'
    endWithStar = p[-1] == '*'

    i = 0 

    parts = [seg for seg in p.split('*') if seg]

    if not startWithStar and parts:
        if not s.startswith(parts[0]):
            return False
        i = len(parts[0])
        parts = parts[1:]
    
    tail = None
    if not endWithStar and parts:
        tail = parts[-1]
        parts = parts[:-1]
    
    for part in parts:
        pos = s.find(part, i)
        if pos == -1:
            return False
        i = pos + len(part)
    
    if tail is not None:
        tailIdx = len(s) - len(tail)
        if i > tailIdx:
            return False
        return s.endswith(tail)
        
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
