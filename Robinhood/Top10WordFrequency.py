"""
Top 10 Word Frequencies
Given a string s, extract all valid words and return the top 10 most frequent words (case-insensitive) with their counts.

Word Definition
A word is the longest consecutive sequence of English letters only:
'A'–'Z' or 'a'–``z`
All non-letter characters are delimiters and should be ignored.

Requirements
Convert words to lowercase before counting.
Return up to 10 pairs formatted as: "[word, frequency]" (string).
Sort results by:
frequency descending
if tie, word lexicographically ascending
If fewer than 10 unique words exist, return all.

Input
s: str

Output
List[str] of up to 10 strings, each in the form "[word, frequency]"
"""
from collections import defaultdict
def topWords(s):
    container = defaultdict(int)
    word = []
    # O(n) n is length of s
    for ch in s:
        if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
            word.append(ch.lower())
        else:
            if word:
                container[''.join(word)] += 1
                word.clear()
    
    if word:
        container[''.join(word)] += 1
        word.clear()
    
    res = [(w, c) for w, c in container.items()]
    res.sort(key = lambda x: (-x[-1], x[0]))
    return res[:10] # time O(klgk)




def run_tests():
    tests = [
        # 1) single word
        ("a", [("a", 1)]),

        # 2) case-insensitive
        ("Hello hello HeLLo", [("hello", 3)]),

        # 3) punctuation as delimiters + tie -> lex order
        ("Hello, hello!! world... WORLD?", [("hello", 2), ("world", 2)]),

        # 4) digits break words
        ("ab12cd AB cd!!", [("ab", 2), ("cd", 2)]),

        # 5) underscore breaks words
        ("a_b a__b", [("a", 2), ("b", 2)]),

        # 6) tie ordering by lexicographical order
        ("b a B A c C", [("a", 2), ("b", 2), ("c", 2)]),

        # 7) fewer than 10 unique
        ("One two three", [("one", 1), ("three", 1), ("two", 1)]),

        # 8) empty / no valid words
        ("", []),
        ("123 !!! ---", []),

        # 9) exactly 10 unique words (all freq=1 => lex order)
        ("j i h g f e d c b a",
         [("a", 1), ("b", 1), ("c", 1), ("d", 1), ("e", 1),
          ("f", 1), ("g", 1), ("h", 1), ("i", 1), ("j", 1)]),

        # 10) 11 unique words => top 10 only (all freq=1 => smallest 10 lex)
        ("k j i h g f e d c b a",
         [("a", 1), ("b", 1), ("c", 1), ("d", 1), ("e", 1),
          ("f", 1), ("g", 1), ("h", 1), ("i", 1), ("j", 1)]),

        # 11) mixed frequencies + tie among non-top words
        ("x x x y y z a a b",
         [("x", 3), ("a", 2), ("y", 2), ("b", 1), ("z", 1)]),
    ]

    for i, (s, expected) in enumerate(tests, 1):
        got = topWords(s)
        assert got == expected, f"Test {i} FAILED\ns={s!r}\n got={got}\n exp={expected}"
    print("All tests passed!")

run_tests()

