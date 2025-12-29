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

def weakest_monster(edges, targets):
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

    # step 3, except all candidate, which can defeat other candidate
    # For each candidate, compute which other candidates it can defeat
    cand_set = set(cand)

    def reachable_candidates(start):
        q = deque([start])
        seen = {start}
        hit = set()
        while q:
            x = q.popleft()
            for y in g[x]:
                if y not in seen:
                    seen.add(y)
                    q.append(y)
                    if y in cand_set:
                        hit.add(y)
        return hit

    reach = {c: reachable_candidates(c) for c in cand}

    # Choose a minimal candidate: it is NOT strictly stronger than another candidate.
    # "c strictly stronger than d" means: c can reach d, but d cannot reach c.
    for c in cand:
        ok = True
        for d in cand:
            if d == c:
                continue
            if d in reach[c] and c not in reach[d]:
                ok = False
                break # c is not a minimal candidate
        if ok:
            return c # c is a minimal candidate

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

def best_defender(edges, targets):
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
