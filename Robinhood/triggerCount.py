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

def triggerCount(edges, entry):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
    
    count = defaultdict(int)
    count[entry] = 1


    # start bfs
    q = deque([entry])
    visited = set([entry]) # visted is set, init value is entry

    while q:
        u = q.popleft()
        for v in g[u]:
            # no matter if visited, still cumulate the count
            count[v] += count[u]
            if v not in visited:
                visited.add(v)
                q.append(v)

    return count # time O(V + E) space O(V + E)

def triggerCountTopo(edges, entry):
    g = defaultdict(list)
    indegree = defaultdict(int)
    nodes = set() # record all nodes
    count = defaultdict(int)
    count[entry] = 1
    for u, v in edges:
        g[u].append(v)
        indegree[v] += 1
        nodes.add(u)
        nodes.add(v)
    
    q = deque()
    for x in nodes:
        if indegree[x] == 0:
            q.append(x)
    
    while q:
        u = q.popleft()
        for v in g[u]:
            indegree[v] -= 1
            count[v] += count[u]
            if indegree[v] == 0:
                q.append(v)
    return count



edges = [
    ("A","B"), ("B","C"), ("B","D"),
    ("C","D"), ("D","E"), ("D","F"),
    ("E","F")
]

print(triggerCount(edges, "A"))
print(triggerCountTopo(edges, "A"))
