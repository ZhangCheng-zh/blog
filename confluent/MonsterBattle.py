"""
You are given a directed “defeat” graph of monsters.
Rule A -> B means A can defeat B.
Defeat is transitive: if A -> B and B -> C, then A -> C.
A monster only “defeats” another monster if there is a path of length ≥ 1 (so it doesn’t automatically defeat itself).

Input
rules: a list of directed edges (winner, loser) or an adjacency map.
targets: a list of monsters that must all be defeatable.

Output
Return any monster that can defeat every monster in targets, and among all such monsters return one that is least-strong:
Monster X is stronger than Y if X can defeat Y (via transitivity).
“Least-strong” means it is not strictly stronger than another valid answer.
If no monster can defeat all targets, return None.

Example
# adjacency list: rules[A] = list of monsters A can defeat directly
rules = {
    "Dragon": ["Zombie", "Goblin"],
    "Zombie": ["Goblin"],
    "Goblin": ["Snake"],
    "Troll": ["Snake"],
}

targets = ["Snake", "Goblin"]

# Expected output (one valid least-strong answer): "Zombie"
"""
from collections import defaultdict, deque

def weakestMonster(edges, targets):
    """
    edges: list of (a, b) meaning a -> b, or dict a -> [b...]
    targets: list of monsters to defeat
    return: a least-strong monster that defeats all targets, else None
    """

    # step1: Build graph + reverse graph
    g = defaultdict(list)
    rg = defaultdict(list)
    nodes = set(targets)

    items = [(a, b) for a, bs in edges.items() for b in bs]

    for a, b in items:
        g[a].append(b)
        rg[b].append(a)
        nodes.add(a)
        nodes.add(b)

    # step 2 find the list of monsters which can defeat all targets
    # Who can defeat a target? (reverse BFS from the target's predecessors)
    def bfs(t):
        q = deque(rg[t])  
        seen = set()
        while q:
            x = q.popleft()
            if x in seen:
                continue
            seen.add(x)
            for p in rg[x]:
                if p not in seen:
                    q.append(p)
        return seen

    # Candidates = intersection of predecessors for all targets
    cand = None
    for t in targets:
        s = bfs(t)
        cand = s if cand is None else (cand & s)
        if not cand:
            return None

    cand = list(cand)


    # ---- Step 3 (simple, correct if DAG) ----
    def reachesOtherCandidate(c):
        q = deque([c])
        seen = {c}
        while q:
            x = q.popleft()
            for y in g.get(x, []):
                if y in seen:
                    continue
                seen.add(y)
                q.append(y)
                if y in cand:      # hit another candidate => c is stronger
                    return True
        return False

    # n loop
    for c in cand:
        # time O(v + E)
        if not reachesOtherCandidate(c):
            return c

    return None



"""
follow-up
# edge list: (A, B, cost) means A can defeat B with cost
edges = [
    ("Dragon", "Zombie", 1),
    ("Dragon", "Goblin", 10),
    ("Zombie", "Goblin", 1),
    ("Goblin", "Snake", 1),
    ("Zombie", "Snake", 10),
    ("Troll", "Goblin", 2),
    ("Troll", "Snake", 2),
]

targets = ["Goblin", "Snake"]

# Expected output (min total cost): "Zombie"
"""
from collections import defaultdict
import heapq

def bestDefender(edges, targets):
    # step 1 Build reversed graph: b -> (a, w)
    rev = defaultdict(list)
    nodes = set(targets)
    for a, b, w in edges:
        rev[b].append((a, w))
        nodes.add(a)
        nodes.add(b)

    # step 2 calculate cost to defeat targets
    # total_cost[x] = sum of dist(x -> t) over all targets t
    total_cost = {x: 0 for x in nodes}
    hit = {x: 0 for x in nodes}  # how many targets this node can reach

    def dijkstra_from_target(t):
        dist = {t: 0}
        pq = [(0, t)]
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            for v, w in rev[u]:
                nd = d + w
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist  # dist[x] = shortest cost x -> t in original graph

    # Run Dijkstra once per target, accumulate
    for t in targets:
        dist_to_t = dijkstra_from_target(t)
        for x, d in dist_to_t.items():
            if x == t: # disallow self defeat
                continue
            total_cost[x] += d
            hit[x] += 1

    # step 3 find the minimum cost for defeating all targets
    k = len(targets)
    ans = None
    best = float("inf")
    for x in nodes:
        if hit[x] == k and total_cost[x] < best:
            best = total_cost[x]
            ans = x

    return ans

# -------------------- Tests for weakestMonster (unweighted) --------------------

# 1) prompt example
rules = {
    "Dragon": ["Zombie", "Goblin"],
    "Zombie": ["Goblin"],
    "Goblin": ["Snake"],
    "Troll": ["Snake"],
}
assert weakestMonster(rules, ["Snake", "Goblin"]) == "Zombie"

# 2) multiple valid least-strong answers (A and B both defeat C, neither defeats the other)
rules = {
    "A": ["C"],
    "B": ["C"],
}
ans = weakestMonster(rules, ["C"])
assert ans in {"A", "B"}

# 3) none can defeat all targets
rules = {
    "A": ["B"],
    "C": ["D"],
}
assert weakestMonster(rules, ["B", "D"]) is None

# 4) targets include a node, but self-defeat not allowed (needs path length >= 1)
rules = {
    "A": ["B"],
    "B": ["C"],
}
assert weakestMonster(rules, ["A"]) is None  # nobody reaches A

# 5) chain: weakest is closest ancestor
rules = {
    "X": ["Y"],
    "Y": ["Z"],
}
assert weakestMonster(rules, ["Z"]) == "Y"   # Y defeats Z, X is stronger

# 6) input as edge list (your current weakestMonster expects dict; this test should fail unless you add normalize)
# edges = [("Dragon", "Zombie"), ("Dragon", "Goblin"), ("Zombie", "Goblin"), ("Goblin", "Snake"), ("Troll", "Snake")]
# assert weakestMonster(edges, ["Snake", "Goblin"]) == "Zombie"


# -------------------- Tests for bestDefender (weighted) --------------------

# 1) prompt follow-up example
edges = [
    ("Dragon", "Zombie", 1),
    ("Dragon", "Goblin", 10),
    ("Zombie", "Goblin", 1),
    ("Goblin", "Snake", 1),
    ("Zombie", "Snake", 10),
    ("Troll", "Goblin", 2),
    ("Troll", "Snake", 2),
]
assert bestDefender(edges, ["Goblin", "Snake"]) == "Zombie"

# 2) single target: choose cheapest path to that target
edges = [
    ("A", "T", 100),
    ("B", "T", 3),
    ("C", "T", 5),
]
assert bestDefender(edges, ["T"]) == "B"

# 3) unreachable target => None
edges = [
    ("A", "B", 1),
]
assert bestDefender(edges, ["C"]) is None

# 4) tie on total cost (either answer acceptable)
edges = [
    ("A", "X", 1),
    ("A", "Y", 1),
    ("B", "X", 1),
    ("B", "Y", 1),
]
ans = bestDefender(edges, ["X", "Y"])
assert ans in {"A", "B"}

# 5) prefers node that can reach all targets (even if cheap for one target)
edges = [
    ("A", "X", 1),
    ("B", "Y", 1),
    ("C", "X", 5),
    ("C", "Y", 5),
]
# A can't reach Y, B can't reach X, only C reaches both
assert bestDefender(edges, ["X", "Y"]) == "C"

print("all tests passed")

"""
Question: Monsters Battle (Tree)
You are given a hierarchy of monsters represented as an n-ary tree.
Each monster node has:
name: unique string
isHostile: boolean (True means hostile)
cost: non-negative integer (only used in follow-up)
children: list of monsters it can defeat directly
Defeat is transitive: a monster defeats all of its descendants.

Part 1
Return all non-hostile monsters that can defeat every hostile monster in the tree.
A monster can defeat a hostile monster if the hostile monster is in its subtree.
Return the answers in any order (or from weakest to strongest).

Follow-up (Part 2)
Return a list of non-hostile monsters with minimum total cost such that together they can defeat all hostile monsters.
If you select a monster, it covers all hostile monsters in its subtree.
You cannot select hostile monsters.
If it’s impossible, return [].
"""

from collections import deque
class MonsterNode:
    def __init__(self, name, isHostile=False, cost=0, children=None):
        self.name = name
        self.isHostile = isHostile
        self.cost = cost
        self.children = children or []


def allDefenders(root):
    # Return all non-hostile monsters that can defeat every hostile monster
    # in a tree, these are exactly the nodes on the path from LCA(hostiles) to root
    # excluding hostile nodes

    parent = {root: None}
    depth = {root: 0}
    hostiles = []

    stack = [root]
    while stack:
        node = stack.pop()
        if node.isHostile:
            hostiles.append(node)
        for child in node.children:
            parent[child] = node
            depth[child] = depth[node] + 1
            stack.append(child)
    
    if not hostiles:
        return []

    def ancestorSet(node):
        s = set()
        cur = node
        while cur is not None:
            s.add(cur)
            cur = parent[cur]
        return s
    
    common = ancestorSet(hostiles[0])
    for h in hostiles[1:]:
        common &= ancestorSet(h)
        if not common:
            return []
    # the deepest node in common nodes
    lca = max(common, key = lambda x: depth[x])

    res = []
    cur = lca
    while cur is not None:
        if not cur.isHostile:
            res.append(cur.name)
        cur = parent[cur]
    return res

def minCostDefenders(root):
    # dp[node] = min cost to cover all hostile nodes in subtree(node)
    INF = 10**30

    # step 1 postorder traversal (children processed before parent)
    postorder = []
    stack = [root]
    while stack:
        node = stack.pop()
        postorder.append(node)
        for child in node.children:
            stack.append(child)
    
    postorder.reverse()

    # dpCost[node] = minimum cost to cover all hostile monsters in node's subtree
    dpCost = {}
    # pick[node] = True if the optimal solution chooses this node itself
    pick = {}

    # step 2 dp compute from leaves up
    for node in postorder:
        if node.isHostile:
            # cant pick hostile
            # also children cannot cover this hostile node itsel
            dpCost[node] = INF
            pick[node] = False
            continue

        # option 1 pick this node -> pay its cost, covers entire subtree
        pickCost = node.cost

        # option 2 do not pick this node
        skipCost = 0
        for child in node.children:
            c = dpCost[child]
            # one child is hostile, this node cannot be skipped
            if c >= INF:
                skipCost = INF
                break 
            skipCost += c

        # choose cheaper option
        if pickCost <= skipCost:
            dpCost[node] = pickCost
            pick[node] = True
        else:
            dpCost[node] = skipCost
            pick[node] = False
    
    if dpCost[root] >= INF:
        return []
    
    res = []

    def collect(node):
        if pick[node]:
            res.append(node.name)
            return
        for child in node.children:
            collect(child)
    collect(root)
    return res


# ---------- helper to build nodes ----------
class MonsterNode:
    def __init__(self, name, isHostile=False, cost=0, children=None):
        self.name = name
        self.isHostile = isHostile
        self.cost = cost
        self.children = children or []


# ---------- Part 1: allDefenders tests ----------
def testAllDefenders():
    # Case 1: no hostile -> []
    root = MonsterNode("A", False, 5, [
        MonsterNode("B", False, 3),
        MonsterNode("C", False, 2),
    ])
    assert allDefenders(root) == []

    # Case 2: single hostile leaf -> path from its parent to root
    h = MonsterNode("H", True)
    b = MonsterNode("B", False, 1, [h])
    root = MonsterNode("A", False, 1, [b])
    # hostiles = [H], common ancestors = {H,B,A}, but exclude hostile nodes
    # result should include B and A (weakest->strongest)
    assert allDefenders(root) == ["B", "A"]

    # Case 3: two hostile leaves in different branches -> LCA to root
    h1 = MonsterNode("H1", True)
    h2 = MonsterNode("H2", True)
    left = MonsterNode("L", False, 1, [h1])
    right = MonsterNode("R", False, 1, [h2])
    root = MonsterNode("A", False, 1, [left, right])
    # LCA is A
    assert allDefenders(root) == ["A"]

    # Case 4: LCA is hostile -> []
    # A* is hostile root, hostiles are under it too, but A cannot be selected in part1 output list
    h1 = MonsterNode("H1", True)
    root = MonsterNode("A", True, 1, [MonsterNode("B", False, 1, [h1])])
    assert allDefenders(root) == []


# ---------- Follow-up: minCostDefenders tests ----------
def testMinCostDefenders():
    # Case 1: example style: choose cheaper internal nodes vs root
    # A(100)
    # ├ B(60) -> covers hostile under B
    # └ C(10) -> covers hostile under C
    h1 = MonsterNode("H1", True)
    h2 = MonsterNode("H2", True)
    b = MonsterNode("B", False, 60, [h1])
    c = MonsterNode("C", False, 10, [h2])
    a = MonsterNode("A", False, 100, [b, c])
    ans = minCostDefenders(a)
    assert set(ans) == {"C", "B"}  # order may vary

    # Case 2: picking parent cheaper than picking children
    # A(5)
    # ├ B(4) -> hostile under B
    # └ C(4) -> hostile under C
    # children cost = 8, parent cost = 5 => pick A
    h1 = MonsterNode("H1", True)
    h2 = MonsterNode("H2", True)
    b = MonsterNode("B", False, 4, [h1])
    c = MonsterNode("C", False, 4, [h2])
    a = MonsterNode("A", False, 5, [b, c])
    assert minCostDefenders(a) == ["A"]

    # Case 3: hostile root -> impossible => []
    root = MonsterNode("A", True, 10, [])
    assert minCostDefenders(root) == []

    # Case 4: hostile internal node must be covered by an ancestor
    # A(7)
    # └ B* (hostile)
    #    └ C(1)
    # Only possible is pick A (cannot pick B)
    c = MonsterNode("C", False, 1)
    b = MonsterNode("B", True, 0, [c])
    a = MonsterNode("A", False, 7, [b])
    assert minCostDefenders(a) == ["A"]

    # Case 5: zero cost nodes
    # A(10)
    # ├ B(0) covers H1
    # └ C(0) covers H2
    h1 = MonsterNode("H1", True)
    h2 = MonsterNode("H2", True)
    b = MonsterNode("B", False, 0, [h1])
    c = MonsterNode("C", False, 0, [h2])
    a = MonsterNode("A", False, 10, [b, c])
    assert set(minCostDefenders(a)) == {"B", "C"}


testAllDefenders()
testMinCostDefenders()
print("all tests passed")
