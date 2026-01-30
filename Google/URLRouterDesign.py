"""
URL Router with * Wildcards (Most-Specific Match)
Design a URL router that maps handler function names to registered URL patterns.

A pattern matches a query URL by segment, where segments are the parts between /.
* is a wildcard segment
* matches exactly one segment (any text in that position)

The router must return the handler for the most specific matching pattern:
    Prefer the match with the fewest * wildcards
    If no pattern matches, return "" (empty string)

Class to Implement
UrlRouter()
    Initialize an empty router.

put(pattern, funcName)
    Register funcName for pattern.
    pattern starts with /
    Each segment is separated by /
    Any segment may be *
    Re-registering the same pattern updates its handler to the latest funcName

get(url) -> String
Return the handler name of the most specific registered pattern that matches url.
    If multiple patterns match, choose the one with the fewest wildcards
    If none match, return ""

Matching Rules
Given:
    pattern = /a/*/c
    url = /a/b/c
They match because:
    segment1: a == a
    segment2: * matches b
    segment3: c == c
A pattern only matches if it has the same number of segments as the URL.

Constraints
pattern and url both:
    start with /
    contain one or more segments
funcName:
    non-empty
    ≤ 20 lowercase English letters
Total calls to put + get ≤ 10^4
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.funcName = ''

class UrlRouter:
    def __init__(self):
        self.root = TrieNode()
    
    def _splitPath(self, path):
        return [seg for seg in path.split('/') if seg]

    def put(self, pattern, funcname): # build trie tree
        node = self.root
        
        for seg in self._splitPath(pattern):
            if seg not in node.children:
                node.children[seg] = TrieNode()
            node = node.children[seg]
        node.funcName = funcname
    
    def get(self, url):
        segs = self._splitPath(url)

        curr = { self.root: 0 }

        # bfs
        for seg in segs:
            nxt = {}
            for node, wildCnt in curr.items():
                exact = node.children.get(seg)

                if exact is not None and exact not in nxt:
                    nxt[exact] = wildCnt 
                
                star = node.children.get('*')
                if star is not None and star not in nxt:
                    nxt[star] = wildCnt + 1
        
            curr = nxt 
            if not curr:
                return ''
            
    
        bestFunc = ''
        bestWild = 10**9

        for node, wildCnt in curr.items():
            if node.funcName != '' and wildCnt < bestWild:
                bestWild = wildCnt
                bestFunc = node.funcName
        
        return bestFunc

router = UrlRouter()
router.put("/*", "oneWildcard")
router.put("/abc/*", "abcOneWildcard")
router.put("/abc/*/*", "abcTwoWildcards")
router.put("/abc/bcd", "exactMatch")

assert router.get("/abc/bcd") == "exactMatch"
assert router.get("/abc/def") == "abcOneWildcard"
assert router.get("/xyz") == "oneWildcard"
assert router.get("/abc/def/ghi") == "abcTwoWildcards"
assert router.get("/def/ghi") == ""
assert router.get("/abc") == "oneWildcard"