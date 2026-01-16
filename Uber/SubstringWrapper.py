"""
Given a string s consisting of multiple words separated by spaces, and a list of strings elements, 
identify the first substring in each word of s that matches any string in elements. 
Once a match is found, wrap the substring in square brackets "[ ]".

Note:
The matching is case-sensitive.
If a word contains multiple potential matches, only the first match (based on the order in elements) should be wrapped.
If no substrings from elements are found in a word, the word remains unchanged.
"""
class Solution:
    def wrapSubstrings(self, s, elements):
        words = s.split(' ')
        res = []

        for word in words:
            wrapped = word
            for pat in elements:
                idx = word.find(pat)
                if idx != -1:
                    wrapped = word[:idx] + '[' + pat + ']' + word[idx + len(pat):]
                    break
            res.append(wrapped)
        
        return ' '.join(res)
    

def runTests():
    sol = Solution()

    assert sol.wrapSubstrings("Uber Eat", ["be", "a"]) == "U[be]r E[a]t"
    assert sol.wrapSubstrings("Basketball", ["Basket", "ball", "a"]) == "[Basket]ball"
    assert sol.wrapSubstrings("Hello World", ["Hi", "Earth"]) == "Hello World"

    # extra tests
    assert sol.wrapSubstrings("aa aa", ["a"]) == "[a]a [a]a"          # first occurrence
    assert sol.wrapSubstrings("Abc abc", ["bc", "B"]) == "A[bc] a[bc]" # case-sensitive

    print("All tests passed!")


runTests()
