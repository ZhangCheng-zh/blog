

"""
Follow-up Question: Phrase Search (Case-Insensitive)

Now extend the previous boolean word search engine to support phrase searching.

You are given a list of documents. Each document has:

a unique docId

a text string

Implement a class DocumentLibrary that supports:

1) Constructor
DocumentLibrary(documents)
documents is a list like: [(docId, text), ...]
Preprocess the documents so that phrase search can be answered efficiently.
The system should scale to up to 1,000,000 documents.

2) Search API
search(phrase) -> list[docId]
Return all document IDs whose text contains the exact phrase, case-insensitive.

A phrase matches only if its words appear in order and consecutively in the document.

You do not need fuzzy matching.

Words are separated by spaces, and the text may also contain punctuation symbols:
. , ? !

Searching must work even when the phrase spans many words.
"""

"""
follow-up
Support boolean queries using AND and OR, such as:
word1 AND word2
word1 AND (word2 OR word3)

The query is already represented as a binary tree:
Leaf nodes are words
Internal nodes are AND or OR
You do not need to parse the query.

Task
Define the query tree node
Traverse the tree to evaluate the query
AND = intersection of document ID sets
OR = union of document ID sets
Return the final list of matching document IDs.
"""

from collections import defaultdict

def tokenize(text) -> list[str]:
    tokens = []
    cur = []
    for ch in text:
        # if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or '0' <= ch <= '9'
        if ch.isalnum():
            cur.append(ch)
        else:
            if cur:
                tokens.append(''.join(cur))
                cur = []
            if ch in ',.?!':
                # single char as token
                tokens.append(ch)
    # append last word
    if cur:
        tokens.append(''.join(cur))
    
    return tokens

class DocumentLibrary:
    def __init__(self, documents):
        # positional inverted index
        # index[token][docId] = positions list(increasing)
        self.index = defaultdict(lambda: defaultdict(list))

        # boolean index: wordToDocIds[token] = {docIds...}
        self.wordToDocIds = defaultdict(set)

        for docId, text in documents:
            tokens = tokenize(text.lower())
            for pos, tok in enumerate(tokens):
                self.index[tok][docId].append(pos)
                self.wordToDocIds[tok].add(docId)
    
    def docsForWord(self, word):
        toks = tokenize(word)
        if len(toks) != 1: # only return for single word
            return set()
        return self.wordToDocIds[toks[0]]


    
    def search(self, phrase: str):
        # return list of docIds containing the phrase
        # phrase must match as consecutive tokens.
        phraseTokens = tokenize(phrase.lower())
        if not phraseTokens:
            return []
        
        # each item in postingsList is dict list [{ docId: postions[] }]
        postingsList = []
        for tok in phraseTokens:
            posting = self.index.get(tok)
            if not posting:
                return []
            postingsList.append(posting)
        
        # candidate docs must contain all tokens
        candidateDocs = set(postingsList[0].keys())
        for posting in postingsList[1:]:
            candidateDocs &= set(posting.keys())
            if not candidateDocs:
                return []
            
        res = []
        for docId in candidateDocs:
            if self._hasPhraseInDoc(docId, postingsList):
                res.append(docId)
        res.sort()
        return res
    def _hasPhraseInDoc(self, docId, postingsList):
        """
        postingsList[i][docId] = positions list for ith token in the phrase
        return True if phrase tokens appear consecutively in this doc
        """
        startCandidates = None
        for i, posting in enumerate(postingsList):
            posList = posting[docId] # list[int]
            starts = { p - i for p in posList } # if ith token appears at position p, the whole phrase to start at s

            # init at i == 0
            if startCandidates is None: 
                startCandidates = starts 
            else: # select out still valid start index
                startCandidates &= starts
            
            if not startCandidates:
                return False 
        
        return True


class OpType:
    WORD = 'WORD'
    AND = 'AND'
    OR = 'OR'

class QueryNode:
    def __init__(self, opType, word=None, left=None, right=None):
        self.opType = opType
        self.word = word
        self.left = left
        self.right = right

def evalBooleanQuery(docLib: DocumentLibrary, root: QueryNode):
    def dfs(node):
        if node.opType == OpType.WORD:
            return docLib.docsForWord(node.word)

        leftSet = dfs(node.left)
        rightSet = dfs(node.right)

        if node.opType == OpType.AND:
            return leftSet & rightSet
        else:
            return leftSet | rightSet
    
    res = list(dfs(root))
    res.sort()
    return res


# --------- Tests for DocumentLibrary (phrase search) ---------

# 1) basic word + phrase
docs = [
    ("1", "Cloud computing is great."),
    ("2", "cloud monitoring dashboards help."),
    ("3", "In the cloud computing is common."),
]
lib = DocumentLibrary(docs)
assert lib.search("cloud") == ["1", "2", "3"]
assert lib.search("cloud monitoring") == ["2"]
assert lib.search("Cloud computing is") == ["1", "3"]
assert lib.search("serverless computing") == []

# 2) order matters + must be consecutive
docs = [
    ("1", "cloud computing is fun"),
    ("2", "cloud is computing fun"),
]
lib = DocumentLibrary(docs)
assert lib.search("cloud computing") == ["1"]
assert lib.search("computing cloud") == []
assert lib.search("cloud computing is") == ["1"]
assert lib.search("cloud is") == ["2"]

# 3) repeated words (multiple matches in one doc)
docs = [
    ("1", "a b a b a b"),
    ("2", "a a b b"),
]
lib = DocumentLibrary(docs)
assert lib.search("a b") == ["1", "2"]
assert lib.search("b a") == ["1"]
assert lib.search("a b a") == ["1"]
assert lib.search("b a b") == ["1"]

# 4) punctuation tokens matter: . , ? !
docs = [
    ("1", "hello, world!"),
    ("2", "hello world"),
    ("3", "hello,world!"),     # no space but tokenizer still splits
    ("4", "hello , world !"),  # spaces around punctuation
]
lib = DocumentLibrary(docs)
assert lib.search("hello, world") == ["1", "3", "4"]
assert lib.search("hello world") == ["2"]
assert lib.search("world!") == ["1", "3", "4"]
assert lib.search("world !") == ["1", "3", "4"]
assert lib.search("hello?") == []

# 5) phrase at start / middle / end
docs = [
    ("1", "start middle end"),
    ("2", "xxx start middle end yyy"),
    ("3", "start middle"),
    ("4", "middle end"),
]
lib = DocumentLibrary(docs)
assert lib.search("start middle") == ["1", "2", "3"]
assert lib.search("middle end") == ["1", "2", "4"]
assert lib.search("start middle end") == ["1", "2"]
assert lib.search("end") == ["1", "2", "4"]

# 6) empty phrase -> []
docs = [("1", "abc def")]
lib = DocumentLibrary(docs)
assert lib.search("") == []

# 7) numeric tokens
docs = [
    ("1", "error 500 happened"),
    ("2", "error 404 happened"),
]
lib = DocumentLibrary(docs)
assert lib.search("error 500") == ["1"]
assert lib.search("500 happened") == ["1"]
assert lib.search("error 4") == []
assert lib.search("error 404 happened") == ["2"]

# 8) case-insensitive
docs = [
    ("1", "HeLLo WoRLd"),
    ("2", "hello world"),
]
lib = DocumentLibrary(docs)
assert lib.search("HELLO") == ["1", "2"]
assert lib.search("hello world") == ["1", "2"]
assert lib.search("WORLD") == ["1", "2"]

documents = [
    (1, "apple banana"),
    (2, "banana orange"),
    (3, "apple orange"),
]
lib = DocumentLibrary(documents)

# apple AND (banana OR orange) => {1,3}
root = QueryNode(
    OpType.AND,
    left=QueryNode(OpType.WORD, word="apple"),
    right=QueryNode(
        OpType.OR,
        left=QueryNode(OpType.WORD, word="banana"),
        right=QueryNode(OpType.WORD, word="orange"),
    ),
)
assert evalBooleanQuery(lib, root) == [1, 3]

# banana AND orange => {2}
root2 = QueryNode(
    OpType.AND,
    left=QueryNode(OpType.WORD, word="banana"),
    right=QueryNode(OpType.WORD, word="orange"),
)
assert evalBooleanQuery(lib, root2) == [2]

# missing word => empty
root3 = QueryNode(OpType.WORD, word="grape")
assert evalBooleanQuery(lib, root3) == []
