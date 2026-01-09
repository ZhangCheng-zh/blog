"""
Trigger Count in a DAG
You are given a directed acyclic graph (DAG).
Each edge A → B means: when A is triggered once, B is triggered once.
There is one entry node.
The entry node is triggered exactly once.
A node may be triggered multiple times if it has multiple parents.
Compute how many times each node is triggered.

Example
Graph
A → B
B → C
B → D
C → D
D → E
D → F
E → F

Entry
A
Output
A: 1
B: 1
C: 1
D: 2
E: 2
F: 4

Explanation
D is triggered by B and C → 2
E is triggered by D twice → 2
F is triggered by D twice and E twice → 4
"""

from collections import defaultdict, deque

def triggerCountError(edges, entry):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
    
    count = defaultdict(int)
    count[entry] = 1


    # start bfs
    q = deque([entry])
    visited = set([entry])

    while q:
        u = q.popleft()
        for v in g[u]:
            count[v] += count[u]
            if v not in visited:
                visited.add(v)
                q.append(v)

    return count 

def triggerCount(edges, entry):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
    
    count = defaultdict(int)
    count[entry] = 1


    # start bfs
    q = deque([entry])

    while q:
        u = q.popleft()
        for v in g[u]:
            count[v] += 1
            q.append(v)

    return count  # time O(2^L) L is layers of 

def triggerCountTopo(edges, entry):
    g = defaultdict(list)
    indegree = defaultdict(int) # record indegree of each node
    nodes = set() # record all nodes
    count = defaultdict(int) # result record
    count[entry] = 1 # start count of entry
    for u, v in edges:
        g[u].append(v)
        indegree[v] += 1
        nodes.add(u)
        nodes.add(v)
    
    q = deque([x for x in nodes if indegree[x] == 0])
    
    while q:
        u = q.popleft()
        for v in g[u]:
            indegree[v] -= 1
            count[v] += count[u]
            if indegree[v] == 0:
                q.append(v)
    return count



# FAIL_BFS_min_counterexample
edges = [("A","B"), ("A","C"), ("C","B"), ("B","D")]
entry = "A"
expected = {"A": 1, "B": 2, "C": 1, "D": 2}
assert {k: v for k, v in triggerCountError(edges, entry).items() if v} == expected
assert {k: v for k, v in triggerCount(edges, entry).items() if v} == expected
assert {k: v for k, v in triggerCountTopo(edges, entry).items() if v} == expected
# Note: triggerCount(edges, entry) is WRONG here (it will give D=1)


# OK_given_example
edges = [
    ("A","B"), ("B","C"), ("B","D"),
    ("C","D"), ("D","E"), ("D","F"),
    ("E","F")
]
entry = "A"
expected = {"A": 1, "B": 1, "C": 1, "D": 2, "E": 2, "F": 4}
assert {k: v for k, v in triggerCount(edges, entry).items() if v} == expected
assert {k: v for k, v in triggerCountTopo(edges, entry).items() if v} == expected

# OK_diamond_then_chain
edges = [("A","B"), ("A","C"), ("B","D"), ("C","D"), ("D","E")]
entry = "A"
expected = {"A": 1, "B": 1, "C": 1, "D": 2, "E": 2}
assert {k: v for k, v in triggerCount(edges, entry).items() if v} == expected
assert {k: v for k, v in triggerCountTopo(edges, entry).items() if v} == expected

# OK_multiple_merges
edges = [
    ("A","B"), ("A","C"),
    ("B","D"), ("C","D"),
    ("B","E"), ("D","E"),
]
entry = "A"
expected = {"A": 1, "B": 1, "C": 1, "D": 2, "E": 3}
assert {k: v for k, v in triggerCount(edges, entry).items() if v} == expected
assert {k: v for k, v in triggerCountTopo(edges, entry).items() if v} == expected

# OK_unreachable_component
edges = [("A","B"), ("B","C"), ("X","Y"), ("Y","Z")]
entry = "A"
expected = {"A": 1, "B": 1, "C": 1}
assert {k: v for k, v in triggerCount(edges, entry).items() if v} == expected
assert {k: v for k, v in triggerCountTopo(edges, entry).items() if v} == expected