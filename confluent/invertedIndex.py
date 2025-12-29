"""
Word Search with AND / OR

You are given a list of documents.
Each document has an ID and a string of words.

Part 1
Design a data structure that, given a word, returns all document IDs that contain this word.

Part 2
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

example:
documents = [
    (1, 'apple banana'),
    (2, 'banana orange'),
    (3, 'apple orange')
]

index = buildIndex(documents)
engine = Query(index)

queryPhrase = Node(
    'AND',
    Node('apple'),
    Node('OR', Node('banana'), Node('orange'))
)

engine.search()
"""
from collections import defaultdict

def buildIndex(document):
    ans = defaultdict(set)
    for docId, doc in document:
        for w in doc.split(' '):
            ans[w].add(docId)
    
    return ans


class Node:
    # if Node is leaf, the val is word, else val is opration type
    def __init__(self, val, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

class Query:
    def __init__(self, index: dict[set]):
        self.index = index
    
    def search(self, root: Node):
        return self._eval(root)
    def _eval(self, node: Node):
        # the node is leaf, return val directly
        if node.left == None and node.right == None:
            return self.index[node.val]
        
        left = self._eval(node.left)
        right = self._eval(node.right)
        
        if node.val == 'AND':
            return left & right 

        if node.val == 'OR':
            return left | right

# time O(total words) O(total postings)
# def buildIndex(documents):
#     index = defaultdict(set)
#     for docId, text in documents:
#         for word in text.split():
#             index[word].add(docId)
#     return index 

# part 2 
# class Node:
#     def __init__(self, val, left = None, right = None):
#         self.val = val
#         self.left = left 
#         self.right = right 

# class Query:
#     def __init__(self, index):
#         self.index = index
#     # time O(N * k) N is number of query nodes, k is size of a posting list; Space O(revursion depth)
#     def search(self, root: Node):
#         return self._eval(root)

#     def _eval(self, node):
#         if node.left is None and node.right is None:
#             return self.index.get(node.val, set())
        
#         left = self._eval(node.left)
#         right = self._eval(node.right)

#         if node.val == 'AND':
#             return left & right
#         if node.val == 'OR':
#             return left | right 


documents = [
    (1, 'apple banana'),
    (2, 'banana orange'),
    (3, 'apple orange')
]

index = buildIndex(documents)

engine = Query(index)

root = Node(
    'AND',
    Node('apple'),
    Node('OR', Node('banana'), Node('orange'))
)

print('apple docIds ', index['apple'])
print('banada docIds ', index['banana'])
print('orange docIds ', index['orange'])

print(engine.search(root))