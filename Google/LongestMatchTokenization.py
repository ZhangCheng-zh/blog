"""
Longest-Match Tokenization with IDs
You are given:
a string text
an array dictionary, where each entry is formatted as "<key>:<id>"
key is a token string, and id is its identifier (string or integer).

Tokenization Rules
Scan text from left to right. At each index i:
Longest Match Priority
Consider all dictionary keys that match starting at text[i].
If multiple keys match, choose the longest key.
Greedy Consumption
After choosing a key, consume all its characters and continue from the next position.
Literal Preservation
If no key matches at i, output the single character text[i] as a literal token and move to i+1.

Output
Return a list of strings where:
if a segment matched a dictionary key, output its corresponding id
otherwise output the literal character

Constraints
1 <= len(text) <= 10^9
0 <= len(dictionary) <= 10^9
All dictionary keys are unique.
"""

from typing import Dict, List

class TrieNode:
    def __init__(self):
        self.children: Dict[str, List] = {}
        self.word: str = None
        self.id: str = None


def longestMatchTokenization(text, dictionary):
    # step 1 build a trie for dictionary
    root = TrieNode()

    for entry in dictionary:
        key, tokenId = entry.split(":", 1)
        node = root
        for ch in key:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = key
        node.id = tokenId

    # step 2 iterate text, find longest match from start letter
    # if find, update start position
    # if not, put start letter into answer array, then update start position
    ans = []
    i = 0 # start match index in text
    n = len(text)

    while i < n:
        node = root # start match with root
        j = i # start match index
        bestId = None
        bestEnd = i

        while j < n and text[j] in node.children:
            node = node.children[text[j]]
            j += 1
            if node.id is not None:
                bestId = node.id 
                bestEnd = j # the end index(exclusive) of that best token
        # text[j] not in node.children
        # pre has match
        if bestId is not None:
            ans.append(bestId)
            i = bestEnd # jump i to the end of the longest match
        # if not word matched start at i
        else:
            ans.append(text[i]) # output the text[i] as a literal token
            i += 1  # i move forward
    
    return ans
    


text1 = "applepiepear"
dict1 = ["app:10", "apple:20", "pie:30"]
assert longestMatchTokenization(text1, dict1) == ["20", "30", "p", "e", "a", "r"]

text2 = "acdebe"
dict2 = ["a:1", "b:2", "cd:3"]
assert longestMatchTokenization(text2, dict2) == ["1", "3", "e", "2", "e"]

text3 = "programmingprogrampropro"
dict3 = ["pro:1", "program:2", "programming:3", "gram:4", "ming:5", "pr:6", "og:7"]
assert longestMatchTokenization(text3, dict3) == ["3", "2", "1", "1"]

print("All tests passed!")

        

