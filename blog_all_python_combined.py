# Combined Python source from blog tree
# Includes all .py files excluding node_modules and __pycache__

# ===== BEGIN FILE: Amazon/MaximumIntervalOverlapCount.py =====

"""
You are given a list of closed intervals on the number line, where each interval 
is represented as a pair [start, end] and includes both endpoints. Two intervals overlap 
at a point if that point lies in both intervals.

Determine the maximum number of intervals that overlap at any single point on 
the number line.

Constraints
1 <= intervals.length <= 10^5
-10^9 <= intervals[i][0] <= intervals[i][1] <= 10^9
"""
def maxOverLap(intervals):
    pipeline = []
    for s, e in intervals:
        pipeline.append((s, 1))
        pipeline.append((e + 1, -1))
    
    res = 0

    pipeline.sort()

    cnt = 0
    for x in pipeline:
        cnt += x[1]
        if cnt > res:
            res = cnt
    return res

# ===== END FILE: Amazon/MaximumIntervalOverlapCount.py =====

# ===== BEGIN FILE: Amazon/UnboundMatrixConnectivity.py =====

"""
### Unbounded Matrix Connectivity

You have an **infinite 2D grid**. Some coordinates contain a **point**, others are empty.
You need to design a class that supports adding points and querying reachability between points.

A **move** from point `A` to point `B` is valid if:
* `A` and `B` are in the **same row** (`rowA == rowB`) **or** the **same column** (`colA == colB`)
* and **both coordinates already contain points**
* Each valid move costs **1 step**

Implement:
* `addPoint(row, col)`
  Add a point at `(row, col)`.
* `isConnected(point1, point2) -> bool`
  Return `True` if there exists a sequence of valid moves from `point1` to `point2`, otherwise `False`.
* `getMinSteps(start, end) -> int`
  Return the **minimum number of steps** to reach `end` from `start`. If impossible, return `-1`.

Notes:
* Coordinates are integers.
* The grid is unbounded.
* Each coordinate pair is unique (no duplicates).
* If either endpoint does not exist as a point, treat it as unreachable.

Example:
Points added: `(0,2)`, `(1,2)`, `(1,4)`
* `isConnected((0,2),(1,4)) = True` via `(1,2)`
* `getMinSteps((0,2),(1,4)) = 2` (`(0,2)->(1,2)->(1,4)`)
"""

from typing import List, Optional
from collections import defaultdict

class UnboundMatrix:
    def __init__(self):
        self.rowDict = defaultdict(list)
        self.colDict = defaultdict(list)

    def addPoint(self, x, y):
        self.rowDict[x].append(y)
        self.colDict[y].append(x)

    def isConnected(self, point1, point2):
        pass

    def getMinSteps(self, start, end):
        pass

# ===== END FILE: Amazon/UnboundMatrixConnectivity.py =====

# ===== BEGIN FILE: Amazon/WeightedIntervalSchedule.py =====

"""
You are given a list of order deliveries scheduled for the day including start time, end time, d
nd dollar amount for completing each order delivery. Assuming only one order can be delivered 
at a time, determine the maximum amount of money that can made from the given deliveries. 
Note: deliveries cannot happen outside the given time constraints for the day

The inputs are as follows: 
start_time = 0 // deliveries for the day cannot start before this time
end_time = 10  // deliveries for the day can’t end after this time
// start time, end time and pay for each order delivery
d_starts = [2, 3, 5, 7] /
d_ends = [6, 5, 10, 11] 
d_pays = [5, 2, 4, 1] 

The output should be an integer representing the maximum amount of money made from deliveries. 
Expected output: 6

# [2, 6, 5] [3, 5, 2] [5, 10, 4] [7, 11, 1]
"""

from bisect import bisect_left

def maxDeliveryPay(starts, ends, pays):
    n = len(starts)
    items = [(s, e, p) for s, e, p in zip(starts, ends, pays)]

    items.sort(key = lambda x: x[1])
    ends.sort()

    # dp[i] mean consider pre ith deliverys, the max pay can get
    # dp[0] = 0 means no pay get with no delivery
    dp = [0] * (n + 1)

    for i in range(n):
        s, e, p = items[i]

        # skip this delivery
        skip = dp[i]

        # pick this delivery
        # find last delivery which is valid, search on [0, i)
        lastValidIdx = bisect_left(ends, s, 0, i)
        # all end in ends[:lastValidIdx] is smaller than s

        take = dp[lastValidIdx] + p

        dp[i + 1] = max(skip, take)
    return dp[-1]


# 0) Empty
assert maxDeliveryPay([], [], []) == 0

# 1) Touching boundary NOT allowed: end == start is invalid
# Can't do (1,3) then (3,5)
assert maxDeliveryPay([1, 3], [3, 5], [5, 6]) == 6

# 2) Gap is allowed: end < start
assert maxDeliveryPay([1, 4], [3, 6], [5, 6]) == 11  # (1,3,5) + (4,6,6)

# 3) Prompt-like example but STRICT rule:
# (3,5) + (5,10) is NOT allowed, so best is (2,6,5) = 5
assert maxDeliveryPay([2, 3, 5], [6, 5, 10], [5, 2, 4]) == 5

# 4) Multiple non-overlapping with gaps
assert maxDeliveryPay([1, 3, 5], [2, 4, 6], [3, 4, 5]) == 12  # 3+4+5

# 5) Nested vs many small: choose many small ones
# (2,3,3)+(4,5,4)+(6,7,5)+(8,9,6) = 18 beats (1,10,10)
assert maxDeliveryPay([1, 2, 4, 6, 8], [10, 3, 5, 7, 9], [10, 3, 4, 5, 6]) == 18

# 6) Overlaps + strict boundary prevents chaining at equality
# (1,4) cannot chain with (4,7)
assert maxDeliveryPay([1, 2, 4], [4, 6, 7], [5, 6, 5]) == 6

# 7) Big profit job + later job with a gap
# (2,4,100) + (6,7,10) = 110
assert maxDeliveryPay([1, 2, 3, 6], [2, 4, 5, 7], [5, 100, 7, 10]) == 110

# 8) Same end times, and a touching-start job (should NOT chain)
# Best is just (3,5,7)
assert maxDeliveryPay([1, 2, 3], [3, 3, 5], [5, 6, 7]) == 7

# 9) Zero/negative pay should be avoidable
assert maxDeliveryPay([1, 3, 5], [2, 4, 6], [0, -5, 10]) == 10

print("✅ All tests passed!")


# ===== END FILE: Amazon/WeightedIntervalSchedule.py =====

# ===== BEGIN FILE: Concurrency/concurrency.py =====

# Coarse-grained locking
import threading

class TicketBooking:
    def __init__(self):
        self._lock = threading.lock()
        self._seatOwners = {}

    def bookSeat(self, seatId, visitorId):
        with self._lock:
            if seatId in self.seatOwner:
                return False
            self._seatOwners[seatId] = visitorId
            return True
        

# Read-write locks
# Also called shared-exclusive lock. It has two modes: read(shared) and write(exclusive)
# they're just reading and can't corrupt each other's view. But the write lock is exclusive.
# When a thread wants to write, it waits for all readers to finish, then blocks everyone else
# until the write completes.

## read preference lock
import threading

class Cache:
    def __init__(self):
        self.dataLock = threading.Lock() # against write
        self.readCount = 0
        self.readCountLock = threading.Lock() # 
        self.data = {}
    
    def get(self, key):
        with self.readCountLock: # very short read lock
            self.readCount += 1
            if self.readCount == 1:
                self.dataLock.acquire()
        # read count lock release, but count remain
        try:
            return self.data.get(key)
        finally:
            # create read count lock again after finish read to update readCount
            with self.readCountLock:
                self.readCount -= 1
                if self.readCount == 0: # not more read, release write lock
                    self.dataLock.release()

    def put(self, key, value):
        with self.dataLock:
            self.data[key] = value

## write preference lock
# Condition = Lock + “wait queue” + “notify”.
class ReadWriteLock:
    def __init__(self):
        self.mu = threading.Lock()
        self.cond = threading.condition(self.mu)
        self.readerCount = 0
        self.writerActive = False
        self.writeWaiting = 0
    
    def acquireRead(self):
        with self.cond:
            # read wait afte active writer
            while self.writerActive or self.writerWaiting > 0:
                self.cond.wait() # wait write
            # no write active and no write waiting, start read
            self.readerCount += 1
    
    def releaseRead(self):
        with self.cond:
            # release one read
            self.readerCount -= 1
            # if all read be released, release rwlock
            if self.readerCount == 0:
                self.cond.notify_all()
    
    def acquireWrite(self):
        with self.cond:
            # put write into wait
            self.writerWaiting += 1
            # if lock used by a write or a read, keep waiting
            while self.writerActive or self.readerCount > 0:
                self.cond.wait()
            # wait end, wait -= 1 and active writing
            self.writerWaiting -= 1
            self.writerActive = True
    
    def releaseWrite(self):
        with self.cond:
            # release active write, then release rwlock, priority to next write, then read
            self.writeActive = False
            self.cond.notify_all()

class Cache:
    def __init__(self):
        self.rwLock = ReadWriteLock()
        self.data = {}

    def get(self, key):
        self.rwLock.acquireRead()
        try:
            return self.data.get(key)
        finally:
            self.rwLock.releaseRead()
    
    def put(self, key, value):
        self.rwLock.acquireWrite()
        try:
            self.data[key] = value
        finally:
            self.rwLock.releaseWrite()
    

# ===== END FILE: Concurrency/concurrency.py =====

# ===== BEGIN FILE: Confluent/LogReader.py =====

"""
Implement a Simple Log Reader
You are given a very large log file on disk (can be GBs). Loading the whole file into memory is not allowed.

Design a class LogReader that supports the following operations efficiently:
1) tail(n) -> str
Return the last n lines of the log file as a string.

Requirements:
Must work for very large files.
Should not read the entire file unless necessary.
You may assume lines are separated by \n.
Use a fixed block_size (default 4096 bytes) and read the file from the end backward.

2) search(phrase) -> bool
Return True if the given UTF-8 string phrase appears anywhere in the file, otherwise False.

Requirements:
Must scan the file in chunks of size block_size.
Must correctly handle the case where the phrase spans across two chunks (cross-boundary matching).
lr = LogReader("app.log")

print(lr.tail(5))          # prints last 5 lines
print(lr.search("ERROR"))  # True/False

lr.close()
"""

import os
class LogReader:
    def __init__(self, filename, blocksize = 4096):
        self.filename = filename
        self.blocksize = blocksize
        self.file = open(filename, 'rb')

    def tail(self, n):
        if n <= 0:
            return ''
        
        f = self.file 
        f.seek(0, os.SEEK_END)
        pos = f.tell()

        newlines = 0

        while pos > 0 and newlines <= n:
            chunk = min(pos, self.blocksize)
            
            pos -= chunk
            f.seek(pos)

            data = f.read(chunk)
            for i in range(chunk - 1, -1, -1):
                if data[i] == ord('\n'):
                    newlines += 1
                if newlines == n + 1:
                    res = pos + i + 1
                    f.seek(res)
                    return f.read().decode('utf-8')
        
        f.seek(0)
        return f.read().decode('utf-8')
    
    def search(self, phrase):
        f = self.file
        if phrase == '':
            return True
        # convert str into bytes
        target = phrase.encode('utf-8')
        
        m = len(target)

        prevTail = b''
        f.seek(0)

        while True:
            data = f.read(self.blocksize)
            if not data:
                return False 
            data = prevTail + data 
            if data.find(target) != -1:
                return True
            
            keep = m - 1
            prevTail = data[-keep:] if keep > 0 else b''

    def close(self):
        self.file.close()



import tempfile
def writeTempLog(text: str) -> str:
    if text and not text.endswith("\n"):
        text += "\n"

    fd, path = tempfile.mkstemp()
    os.close(fd)
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))
    return path

# tail: always ends with newline
path = writeTempLog("a\nb\nc\nd\ne")
lr = LogReader(path, 4)  # small block forces backward multi-read
assert lr.tail(2).splitlines() == ["d", "e"]
assert lr.tail(5).splitlines() == ["a", "b", "c", "d", "e"]
assert lr.tail(10).splitlines() == ["a", "b", "c", "d", "e"]
assert lr.tail(0) == ""
lr.close()
os.remove(path)

# tail: single line + newline
path = writeTempLog("onlyOneLine")
lr = LogReader(path, 3)
assert lr.tail(1).splitlines() == ["onlyOneLine"]
lr.close()
os.remove(path)

# tail: empty file (no newline)
path = writeTempLog("")
lr = LogReader(path, 8)
assert lr.tail(3) == ""
lr.close()
os.remove(path)

# search: basic present/absent
path = writeTempLog("hello world\nERROR here\nbye")
lr = LogReader(path, 8)
assert lr.search("ERROR") is True
assert lr.search("MISSING") is False
lr.close()
os.remove(path)

# search: cross-boundary match (phrase spans chunks)
path = writeTempLog("abcde")  # with block=4, "abcd" + "e\n"
lr = LogReader(path, 4)
assert lr.search("cde") is True
assert lr.search("de\n") is True
assert lr.search("de") is True
assert lr.search("ab") is True
assert lr.search("cdef") is False
lr.close()
os.remove(path)

# ===== END FILE: Confluent/LogReader.py =====

# ===== BEGIN FILE: Confluent/MonsterBattle.py =====

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


# ===== END FILE: Confluent/MonsterBattle.py =====

# ===== BEGIN FILE: Confluent/Sudoku.py =====

"""
Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

Each row must contain the digits 1-9 without repetition.
Each column must contain the digits 1-9 without repetition.
Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.
Note:

A Sudoku board (partially filled) could be valid but is not necessarily solvable.
Only the filled cells need to be validated according to the mentioned rules.
 

Example 1:


Input: board = 
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true
Example 2:

Input: board = 
[["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: false
Explanation: Same as Example 1, except with the 5 in the top left corner being modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is invalid.
 

Constraints:

board.length == 9
board[i].length == 9
board[i][j] is a digit 1-9 or '.'.
"""
from typing import List

def isValidSudoku(board: List[List[str]]) -> bool:
    rows = [set() for i in range(9)]
    cols = [set() for i in range(9)]
    sub = [set() for i in range(9)]
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.': continue
            c = int(board[i][j])
            if c in rows[i] or c in cols[j] or c in sub[(i // 3) * 3 + j // 3]:
                return False
            else:
                rows[i].add(c)
                cols[j].add(c)
                sub[(i // 3) * 3 + j // 3].add(c)
    return True     


"""
Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:

Each of the digits 1-9 must occur exactly once in each row.
Each of the digits 1-9 must occur exactly once in each column.
Each of the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
The '.' character indicates empty cells.

 

Example 1:


Input: board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
Output: [["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]]
Explanation: The input board is shown above and the only valid solution is shown below:


Constraints:

board.length == 9
board[i].length == 9
board[i][j] is a digit or '.'.
It is guaranteed that the input board has only one solution.
"""
def solveSudoku(self, board: List[List[str]]) -> None:
    """
    Do not return anything, modify board in-place instead.
    """
    # first check the sudoku has answer
    # if not isValidSudoku(board): return False

    # record already used numbers for each row col and sub
    rows = [set() for i in range(9)]
    cols = [set() for i in range(9)]
    sub = [set() for i in range(9)]
    emptyCells = []

    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                emptyCells.append((i, j))
            else:
                c = int(board[i][j])
                rows[i].add(c)
                cols[j].add(c)
                sub[(i // 3) * 3 + j // 3].add(c)

    # dfs backtrack fill emptycells one by one
    def dfs(idx) -> bool:
        # filled all emptyCell with valid number
        # find answer
        if idx == len(emptyCells):
            return True

        i, j = emptyCells[idx]

        # try all candidates in target cell
        for x in range(1, 10):
            # x already used
            if x in rows[i] or x in cols[j] or x in sub[(i // 3) * 3 + j // 3]:
                continue
            
            board[i][j] = str(x)
            rows[i].add(x)
            cols[j].add(x)
            sub[(i // 3) * 3 + j // 3].add(x)

            if dfs(idx + 1):
                return True
            
            # restore
            rows[i].remove(x)
            cols[j].remove(x)
            sub[(i // 3) * 3 + j // 3].remove(x)

        return False
    
    dfs(0)

# ===== END FILE: Confluent/Sudoku.py =====

# ===== BEGIN FILE: Confluent/TimeBasedKVStore.py =====

"""
Design a data structure WindowedMap that stores (key, value) events and supports queries over the last 5 minutes.

Window rule

At query time t, an entry (key, value, ts) is valid if ts >= t - 5min.

APIs
addEvent(key: str, val: int, timestamp: int) -> None
getKey(key: str, timestamp: int) -> int        # if key valid in last 5min, return val; else throw/raise
delete(key: str) -> None
avg(timestamp: int) -> float                   # average of all valid values in last 5min; if none, return 0.0

Notes

Each key keeps only its most recent event (a new addEvent replaces the old one).

You may assume timestamp values passed to addEvent are non-decreasing.

Aim for high performance:

addEvent, getKey, delete: O(1) amortized

avg: O(1) amortized
"""

# Node for linkedList
class Node:
    def __init__(self, key='', val = 0, ts = 0):
        self.key, self.val, self.ts = key, val, ts
        self.prev = self.next = None 

class WindowedMap:
    def __init__(self, window=300):
        self.window = window 
        self.mp = {}
        self.dummy = Node() # dummy is head and tail node
        self.dummy.prev = self.dummy.next = self.dummy
        self.sum = 0 # record sum of val
        self.cnt = 0 # record count of node

    # remove node from linkedlist
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    # add node at head of list
    def _add_front(self, node):
        node.prev = self.dummy
        node.next = self.dummy.next
        self.dummy.next.prev = node
        self.dummy.next = node 
    
    def _purge(self, t):
        cutoff = t - self.window + 1
        while self.dummy.prev != self.dummy and self.dummy.prev.ts < cutoff:
            old = self.dummy.prev
            self._remove(old)
            self.mp.pop(old.key, None)
            self.sum -= old.val
            self.cnt -= 1
    
    def put(self, key, val, t):
        self._purge(t)

        if key in self.mp:
            old = self.mp.pop(key)
            self._remove(old)
            self.sum -= old.val
            self.cnt -= 1
        
        node = Node(key, val, t)
        self._add_front(node)
        self.mp[key] = node
        self.sum += val
        self.cnt += 1
    
    def get(self, key, t):
        self._purge(t)
        node = self.mp.get(key)
        if not node:
            raise KeyError('not found key')

        node.ts = t
        self._remove(node)
        self._add_front(node)

        return node.val

    def delete(self, key):
        node = self.mp.pop(key, None)
        if not node:
            return 
        self._remove(node)
        self.sum -= node.val
        self.cnt -= 1

    def avg(self, t):
        self._purge(t)
        return 0.0 if self.cnt == 0 else self.sum / self.cnt
    
wm = WindowedMap(window=5)

wm.put("a", 10, 1)
wm.put("b", 20, 2)

assert wm.get("a", 2) == 10          # access updates ts(a)=2
assert abs(wm.avg(2) - 15.0) < 1e-9     # a(2), b(2)

# at t=6, window is [2..6], b(ts=2) still valid, a(ts=2) valid
assert abs(wm.avg(6) - 15.0) < 1e-9

# access a at t=6, refresh ts(a)=6
assert wm.get("a", 6) == 10

# at t=7, window is [3..7], b(ts=2) expires, a(ts=6) stays
assert abs(wm.avg(7) - 10.0) < 1e-9

try:
    wm.get("b", 7)
    assert False
except KeyError:
    pass

wm.delete("a")
assert abs(wm.avg(7) - 0.0) < 1e-9



"""
Use N independent WindowedMaps (each with its own lock), and route keys by hash:
reduces contention a lot
still “global lock” per shard, but not for the whole system
avg() becomes: sum averages across shards (or sum/cnt across shards) — requires reading each shard (still fine).
"""
import threading

# node for linkedlist
class Node:
    def __init__(self, key='', val = 0, ts = 0):
        self.key, self.val, self.ts = key, val, ts
        self.prev = self.next = None 

class Shard:
    def __init__(self, window: int):
        self.window = window
        self.mp = {}
        self.dummy = Node()
        self.dummy.prev = self.dummy.next = self.dummy
        self.sum = 0
        self.cnt = 0
        self.lock = threading.RLock()
    
    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_front(self, node):
        node.prev = self.dummy
        node.next = self.dummy.next
        self.dummy.next.prev = node 
        self.dummy.next = node 
    
    def _purge(self, t):
        cutoff = t - self.window + 1
        while self.dummy.prev != self.dummy and self.dummy.prev.ts < cutoff:
            old = self.dummy.prev
            self._remove(old)
            self.mp.pop(old.key, None)
            self.sum -= old.val
            self.cnt -= 1
    
    def put(self, key, val, t):
        with self.lock:
            self._purge(t)
            if key in self.mp:
                old = self.mp.pop(key)
                self._remove(old)
                self.sum -= old.val
                self.cnt -= 1
            
            node = Node(key, val, t)
            self._add_front(node)
            self.mp[key] = node
            self.sum += ValueError
            self.cnt += 1
    
    def get(self, key, t):
        with self.lock:
            self._purge(t)
            node = self.mg.get(key)
            if not node:
                raise KeyError('not found key')

            # refresh on access
            node.ts = t
            self._remove(node)
            self._add_front(node)
            return node.val 
    
    def delete(self, key):
        with self.lock:
            node = self.mp.pop(key, None)
            if not node:
                return
            self._remove(node)
            self.sum -= node.val
            self.cnt -= 1
    
    def snapshot_sum_cnt(self, t) -> tuple[int, int]:
        with self.lock:
            self._purge(t)
            return self.sum, self.cnt
        
class ShardedWindowedMap:
    def __init__(self, window = 300, shards = 16):
        self.window = window
        self.shards = [Shard(window) for _ in range(shards)]
        self.n = shards
    
    def _idx(self, key) -> str:
        return hash(key) % self.n 
    
    def put(self, key, val, t):
        self.shards[self._idx(key)].put(key, val, t)
    
    def get(self, key, t):
        return self.shards[self._idx(key)].get(key, t)

    def delete(self, key):
        self.shards[self._idx(key)].delete(key)

    def avg(self, t):
        totalSum, totalCnt = 0, 0
        for sh in self.shards:
            s, c = sh.snapshot_sum_cnt(t)
            totalSum += s
            totalCnt += c
        return 0,0 if totalCnt == 0 else totalSum/ totalCnt
    
    # strong consistent snapshot avg
    def avg(self, t: int) -> float:
        # 1) acquire all shard locks in a fixed order (avoid deadlock)
        for sh in self.shards:
            sh.lock.acquire()

        try:
            total_sum, total_cnt = 0, 0
            # 2) now it's a consistent snapshot: no shard can change while we read
            for sh in self.shards:
                sh._purge(t)              # safe: we already hold sh.lock
                total_sum += sh.sum
                total_cnt += sh.cnt

            return 0.0 if total_cnt == 0 else total_sum / total_cnt
        finally:
            # 3) release in reverse order (common practice)
            for sh in reversed(self.shards):
                sh.lock.release()


# ===== END FILE: Confluent/TimeBasedKVStore.py =====

# ===== BEGIN FILE: Confluent/VaridicFunction.py =====

# class Function:
#     def __init__(self, name, argument_types):
#         self.name = name 
#         self.argument_types = argument_types
    
#     def __repr__(self):
#         return f"Function<{self.name}>"

# class FunctionLibrary:
#     def __init__(self):
#         self.

    
#     def register(self, list_of_function):
#         pass # todo
    
#     def find_matches(self, argument_types): # time complexity: O(m) m is size of functionLibrary space: O(1)
#         pass# todo

"""
some test
flib = FunctionLibrary()
flib.register([
Function("funA", ["Boolean", "Integer"]),
Function("funB", ["Integer"]),
Function("funC", ["Integer"])  
])

assert flib.find_matches(['Bool])
"""



### **Extended Version (with `isVariadic` support)**


"""
register([
    funA: {["Boolean", "Integer"], isVariadic: False},
    funB: {["Integer"], isVariadic: False},
    funC: {["Integer"], isVariadic: True}
])

findMatches(["Boolean", "Integer"]) -> [funA]
findMatches(["Integer"]) -> [funB, funC]
findMatches(["Integer", "Integer", "Integer"]) -> [funC]
"""

from collections import defaultdict

class Function:
    def __init__(self, name, argument_types, is_variadic):
        self.name = name
        self.argument_types = argument_types
        self.isVariadic = is_variadic

    def __repr__(self):
        return "Function<{}>".format(self.name)


class FunctionLibrary:
    def __init__(self):
        self.nonVariadic = defaultdict(list) # tuple -> [Function]
        self.isVariadic = defaultdict(list) # tuple -> [Function]

    def register(self, list_of_functions): # time: O(n) n is count of function
        for f in list_of_functions:
            sig = tuple(f.argument_types)
            if not f.isVariadic:
                self.nonVariadic[sig].append(f)
            else:
                prefix = sig[:-1]
                varType = sig[-1]
                self.isVariadic[(prefix, varType)].append(f)

    def findMatches(self, argument_types):
        args = tuple(argument_types)
        matches = []

        # find all matched nonVariadic function
        matches.extend(self.nonVariadic[args])

        if args:
            prefix = args[:-1]
            last = args[-1]
            # find the head of same arg tail
            s = len(args) - 1
            while s > 0 and args[s - 1] == last:
                s -= 1
            
            for j in range(s, len(args)):
                prefix = args[:j]
                matches.extend(self.isVariadic[(prefix, last)])
        print([f.name for f in matches])
        return [f.name for f in matches] # each match time complexity:  O(k) k is length of argument_types of find_match


flib =  FunctionLibrary() 
fa = Function('funA', ["Boolean", "Integer"], False)
fb = Function('funB', ["Integer"], False)
fc = Function('funC', ["Integer"], True)
flib.register([fa, fb, fc]) 

assert flib.findMatches(["Boolean", "Integer"]) == ['funA']
assert flib.findMatches(["Integer"]) == ['funB', 'funC']
assert flib.findMatches(["Integer", "Integer", "Integer"]) == ['funC']

# ===== END FILE: Confluent/VaridicFunction.py =====

# ===== BEGIN FILE: Confluent/infiniteQueue.py =====

"""
An infinite queue is a data structure that dynamically expands to hold an unlimited number of elements. Implement an infinite queue specifically for integers, supporting the following operations:

offer(int val): Add an integer to the tail of the queue.
int poll(): Removes and returns the integer at the front of the queue. If the queue is empty, returns -1.
int getRandom(): Returns a random integer from the queue. If the queue is empty, returns -1.
All operations must be implemented to run in O(1) time.

Constraints:

The number of operations will not exceed 105.
All integers are within the range [-109, 109].
Example 1:

Input:
["InfiniteQueue", "offer", "offer", "offer", "offer", "offer", "getRandom", "getRandom", "getRandom", "poll", "poll", "poll", "poll", "poll"]
[[], [1], [2], [3], [4], [5], [], [], [], [], [], [], [], []]

Output:
[null, null, null, null, null, null, 3, 1, 5, 1, 2, 3, 4, 5]
"""

import random
# a infinite queue for integers
class InfiniteQueue:
    def __init__(self):
        self.capacity = 4 # when all used, double the size, when usage down to 1/4 size, shrink capacity to half
        self.size = 0
        self.buf = [0] * self.capacity
        self.head = 0
    
    def _resize(self, newCapacity):
        newBuf = [0] * newCapacity
        
        for i in range(self.size):
            newBuf[i] = self.buf[(self.head + i) % self.capacity]
        
        self.buf = newBuf
        self.capacity = newCapacity
        self.head = 0



    # add an integer to the tail of the queue
    def offer(self, val): # time: O(1)
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        
        tail = (self.head + self.size) % self.capacity 
        self.buf[tail] = val
        self.size += 1

    # removes and returns the integer at the front of the queue.
    def poll(self): # time: O(1)
        if self.size == 0:
            return -1

        val = self.buf[self.head]
        self.head = (self.head + 1) % self.capacity 
        self.size -= 1

        if self.capacity > 4 and self.size <= self.capacity // 4:
            self._resize(self.capacity // 2) 
        
        return val

    # return a random integer from the queue
    def getRandom(self): # time: O(1)
        if self.size == 0:
            return -1
        # random.random return float
        # below can use random.randint(0, size - 1)
        k = random.randrange(self.size)

        return self.buf[(self.head + k) % self.capacity]

import random


# basic offer/poll order
q = InfiniteQueue()
q.offer(1); q.offer(2); q.offer(3)
assert q.poll() == 1
assert q.poll() == 2
assert q.poll() == 3
assert q.poll() == -1  # empty

# wrap-around without resize
q = InfiniteQueue()
q.offer(10); q.offer(20); q.offer(30); q.offer(40)
assert q.poll() == 10
assert q.poll() == 20
q.offer(50); q.offer(60)  # should wrap in buffer
assert q.poll() == 30
assert q.poll() == 40
assert q.poll() == 50
assert q.poll() == 60
assert q.poll() == -1

# grow (forces resize up)
q = InfiniteQueue()
for i in range(1, 9):  # > initial capacity 4
    q.offer(i)
for i in range(1, 9):
    assert q.poll() == i
assert q.poll() == -1

# getRandom returns an element in queue
q = InfiniteQueue()
q.offer(7); q.offer(8); q.offer(9)
random.seed(0)
x = q.getRandom()
assert x in (7, 8, 9)

# getRandom on empty
q = InfiniteQueue()
assert q.getRandom() == -1


# ===== END FILE: Confluent/infiniteQueue.py =====

# ===== BEGIN FILE: Confluent/invertedIndex.py =====



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


# ===== END FILE: Confluent/invertedIndex.py =====

# ===== BEGIN FILE: Confluent/subsetSum.py =====

"""
nums = [a1, a2, ..., an]
target = T

Q1 if has a subset of nums which sum is target
Q2 return a valid subset
"""






from functools import cache

# time O(2^n) space O(n)
def subsetSum(nums, target):
    n = len(nums)
    # check if pick the idx num, and presum is temp sum
    def backtrack(idx, presum):
        if presum == target:
            return True
        # no more num can be picked or temp sum already larger than target
        if idx >= n or presum > target:
            return False
        
        # not pick num
        if backtrack(idx + 1, presum) or backtrack(idx + 1, presum + nums[idx]):
            return True
        
        return False

    return backtrack(0, 0)

# time: O(n * target) space O(target)
def subsetSumDP(nums, target):
    n = len(nums)
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        # why reverse iterate, because need smaller target dp
        for t in range(target, num - 1, -1):
            dp[t] = dp[t] or dp[t - num] # if not pick target num or pick target num
    
    return dp[target]

# time: O(n * target) space O(n * target)
def subsetSumDP2D(nums, target):
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True

    for i in range(n + 1):
        dp[i][0] = True

    for i in range(n):
        start = nums[i]
        for t in range(target + 1):
            dp[i + 1][t] = dp[i][t] or (t >= start and dp[i][t - start])
    
    return dp[-1][-1]


print(subsetSumDP2D([1,2,3,4], 3))
print(subsetSumDP2D([1,2,3,4], 10))
print(subsetSumDP2D([1,2,3,4], 12))
print(subsetSumDP2D([1,3,5], 2))

# time O(2^n) space O(n)
def subsetSumPath(nums, target):
    n = len(nums)

    def backtrack(idx, path):
        if sum(path) == target:
            return True,path[:]
        
        if idx >= n or sum(path) > target:
            return False, []
        
        # not pick nums[idx]
        valid, res = backtrack(idx + 1, path)
        if valid:
            return valid, res

        # pick nums[idx]
        path.append(nums[idx])

        valid, res = backtrack(idx + 1, path)
        if valid:
            return valid, res

        # restore
        path.pop()

        return False, []
    
    return backtrack(0, [])
    

# time: O(n * target) space O(n * target)
def subsetSumPathDP2D(nums, target):
    # dp[i][j] = -1 -> impossible using first i numbers to make sum j
    #             0 -> possible, and we did not pick nums[i - 1]
    #             1 -> possible, and we did pick nums[i - 1]
    n = len(nums)
    dp = [[-1] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = 0 # no num, target is 0, so no pick

    for i in range(n):
        num = nums[i]
        for j in range(target + 1):
            # not pick
            # without num, can still match sum j
            if dp[i][j] != -1:
                dp[i + 1][j] = 0

            # pick
            if j >= num and dp[i][j - num] != -1:
                dp[i + 1][j] = 1
    
    if dp[-1][-1] == -1:
        return False, []
    
    path = []
    i, j = n, target
    while i > 0 and j >= 0:
        choice = dp[i][j]
        if choice == 1:
            num = nums[i - 1]
            path.append(num)
            j -= num
        i -= 1
    
    path.reverse()
    return True, path

def subsetSumPathDP(nums, target):
    dp = [-1] * (target + 1)
    dp[0] = 1 # means target == 0 always has answer

    for i, num in enumerate(nums):
        for t in range(target, num - 1, -1):
            if dp[t] == -1 and dp[t - num] != -1:
                dp[t] = i
    
    if dp[target] == -1:
        return False, []
    
    res = []
    t = target
    while t > 0:
        res.append(nums[dp[t]])
        t -= nums[dp[t]]
    
    return True, res[::-1]

print(subsetSumPathDP([1,2,3,4], 3))
print(subsetSumPathDP([1,2,3,4], 10))
print(subsetSumPathDP([1,2,3,4], 12))
print(subsetSumPathDP([1,3,5], 2))

# ---------- More tests for subset sum (exists + path) ----------

def assertExistsAll(nums, target, expected):
    assert subsetSum(nums, target) == expected
    assert subsetSumDP(nums, target) == expected
    assert subsetSumDP2D(nums, target) == expected

def assertPathAll(nums, target, expectedExists):
    ok1, path1 = subsetSumPath(nums, target)
    ok2, path2 = subsetSumPathDP2D(nums, target)
    ok3, path3 = subsetSumPathDP(nums, target)

    assert ok1 == expectedExists
    assert ok2 == expectedExists
    assert ok3 == expectedExists

    if expectedExists:
        assert sum(path1) == target
        assert sum(path2) == target
        assert sum(path3) == target
        # each picked element must come from nums (multiset check is complex; keep it simple)
        for x in path1: assert x in nums
        for x in path2: assert x in nums
        for x in path3: assert x in nums
    else:
        assert path1 == []
        assert path2 == []
        assert path3 == []

# 1) empty nums
assertExistsAll([], 0, True)
assertPathAll([], 0, True)      # empty subset
assertExistsAll([], 5, False)
assertPathAll([], 5, False)

# 2) target = 0 (should always be True: empty subset)
assertExistsAll([1, 2, 3], 0, True)
assertPathAll([1, 2, 3], 0, True)

# 3) single element
assertExistsAll([7], 7, True)
assertPathAll([7], 7, True)
assertExistsAll([7], 3, False)
assertPathAll([7], 3, False)

# 4) duplicates (0/1 subset sum still ok)
assertExistsAll([2, 2, 2], 4, True)
assertPathAll([2, 2, 2], 4, True)
assertExistsAll([2, 2, 2], 6, True)
assertPathAll([2, 2, 2], 6, True)
assertExistsAll([2, 2, 2], 1, False)
assertPathAll([2, 2, 2], 1, False)

# 5) includes zero
assertExistsAll([0, 0, 5], 5, True)
assertPathAll([0, 0, 5], 5, True)
assertExistsAll([0, 0, 0], 0, True)
assertPathAll([0, 0, 0], 0, True)

# 6) multiple solutions exist (any one is acceptable)
assertExistsAll([1, 2, 3, 4, 5], 9, True)   # 4+5 or 2+3+4 etc.
assertPathAll([1, 2, 3, 4, 5], 9, True)

# 7) larger target near sum(nums)
assertExistsAll([3, 4, 6, 10], 23, True)    # all
assertPathAll([3, 4, 6, 10], 23, True)
assertExistsAll([3, 4, 6, 10], 24, False)
assertPathAll([3, 4, 6, 10], 24, False)

# 8) “tight” target that needs skipping big numbers
assertExistsAll([8, 1, 2, 9], 3, True)      # 1+2
assertPathAll([8, 1, 2, 9], 3, True)

# 9) classic subset-sum set
nums = [3, 34, 4, 12, 5, 2]
assertExistsAll(nums, 9, True)             # 4+5 or 3+4+2
assertPathAll(nums, 9, True)
assertExistsAll(nums, 30, False)
assertPathAll(nums, 30, False)

# 10) stress-ish small: many 1s
nums = [1] * 20
assertExistsAll(nums, 20, True)
assertPathAll(nums, 20, True)
assertExistsAll(nums, 21, False)
assertPathAll(nums, 21, False)


# ===== END FILE: Confluent/subsetSum.py =====

# ===== BEGIN FILE: Confluent/wasAlive.py =====

"""
Given timestamps for a key, determine whether within a sliding 500ms window starting at `start`, 
divided into 5 fixed 100ms buckets, the key appears in **at least 3 consecutive buckets**.
It is essentially a **time-bucket / sliding-window continuity detection** problem.
"""
from bisect import bisect_left
def wasAlive(records, key, start):
    buckets = [False] * 5
    for k, t in records:
        if k != key:
            continue
        if start <= t <= start + 499:
            idx = (t - start) // 100
            buckets[idx] = True
    for i in range(3):
        if all(buckets[i: i + 3]):
            return True
    return False


# Basic: 3 consecutive buckets (0,1,2) => True
records = [("a", 0), ("a", 101), ("a", 250)]
assert wasAlive(records, "a", 0) is True  # buckets: [T,T,T,F,F]

# Non-consecutive (0,2,4) => False
records = [("a", 0), ("a", 250), ("a", 450)]
assert wasAlive(records, "a", 0) is False  # [T,F,T,F,T]

# Exactly 3 consecutive buckets (2,3,4) => True
records = [("a", 200), ("a", 320), ("a", 499)]
assert wasAlive(records, "a", 0) is True  # [F,F,T,T,T]

# Boundary: include start and start+499, exclude start+500
records = [("a", 0), ("a", 99), ("a", 100), ("a", 199), ("a", 200)]
assert wasAlive(records, "a", 0) is True  # [T,T,T,F,F]
records = [("a", 500), ("a", 600), ("a", 700)]
assert wasAlive(records, "a", 0) is False  # all out of window

# Multiple events in same bucket still counts as one bucket => True
records = [("a", 10), ("a", 20), ("a", 110), ("a", 115), ("a", 210)]
assert wasAlive(records, "a", 0) is True  # [T,T,T,F,F]

# Wrong key ignored => False
records = [("b", 0), ("b", 120), ("b", 240), ("b", 360)]
assert wasAlive(records, "a", 0) is False

# Start offset: window [1000..1499], buckets 0..4 => True (0,1,2)
records = [("a", 1000), ("a", 1100), ("a", 1299)]
assert wasAlive(records, "a", 1000) is True  # [T,T,T,F,F]

# Start offset: consecutive buckets (1,2,3) => True
records = [("a", 1100), ("a", 1250), ("a", 1350)]
assert wasAlive(records, "a", 1000) is True  # [F,T,T,T,F]

# Only 2 consecutive buckets => False
records = [("a", 0), ("a", 150), ("a", 399)]
assert wasAlive(records, "a", 0) is False  # [T,T,F,T,F]

# Empty records => False
records = []
assert wasAlive(records, "a", 0) is False


def wasAliveFast(records, key, start, bucketSize = 100, bucketCount = 5, needConsecutive = 3):
    tw = [t for k, t in records if k == key]
    tw.sort()

    buckets = [False] * bucketCount
    for i in range(bucketCount):
        left = start + i * bucketSize
        right = left + bucketSize - 1
        idx = bisect_left(tw, left)
        # if has record in target bucket of tw, heartbeat true
        buckets[i] = (idx < len(tw) and tw[idx] <= right)
    

    run = 0
    for b in buckets:
        if b:
            run += 1
        else:
            run = 0
        if run >= needConsecutive:
            return True
    return False

# 11) custom params: need 4 consecutive buckets
records = [("a", 0), ("a", 100), ("a", 200), ("a", 300)]
assert wasAliveFast(records, "a", 0, needConsecutive=4) is True
records = [("a", 0), ("a", 100), ("a", 200)]
assert wasAliveFast(records, "a", 0, needConsecutive=4) is False

# 12) custom params: bucketSize=50ms, 10 buckets, need 3 consecutive
records = [("a", 0), ("a", 60), ("a", 120)]  # buckets 0,1,2 with size 50
assert wasAliveFast(records, "a", 0, bucketSize=50, bucketCount=10, needConsecutive=3) is True

# ===== END FILE: Confluent/wasAlive.py =====

# ===== BEGIN FILE: Confluent/wildcardMatch-0.py =====

"""
Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:

'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).
The matching should cover the entire input string (not partial).

Example 1:

Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".
Example 2:

Input: s = "aa", p = "*"
Output: true
Explanation: '*' matches any sequence.
Example 3:

Input: s = "cb", p = "?a"
Output: false
Explanation: '?' matches 'c', but the second letter is 'a', which does not match 'b'.
"""

def wildcardMatch(s, p):
    m, n = len(s), len(p)
    # dp[i][j] mean if s[:i] and p[:j] is match
    # dp[0][0] is empty match empty
    dp = [[False for _ in range(n + 1)] for _ in range(m + 1)]

    # init condition
    dp[0][0] = True 

    for j in range(n):
        if p[j] == '*':
            dp[0][j + 1] = True
        else:
            break
    
    for i in range(m):
        for j in range(n):
            if p[j] == '*':
                dp[i + 1][j + 1] = dp[i + 1][j] | dp[i][j + 1]
            if p[j] == '?' or s[i] == p[j]:
                dp[i + 1][j + 1] = dp[i][j]
    # time O(mn) space O(mn)
    return dp[m][n]

assert wildcardMatch('aa', 'a') == False
assert wildcardMatch('aa', '*') == True
assert wildcardMatch('aa', '?a') == True
assert wildcardMatch('aa', '?b') == False
assert wildcardMatch('aa', '?*') == True

# ===== END FILE: Confluent/wildcardMatch-0.py =====

# ===== BEGIN FILE: Confluent/wildcardMatch-1.py =====

"""
Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:

'.' Matches any single character.​​
'*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial).


Example 1:
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".

Example 2:
Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".

Example 3:
Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.)".
"""

def wildcardMatch(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    # init condition
    dp[0][0] = True
    
    for j in range(1, n, 2):
        if p[j] != '*':
            break
        dp[0][j + 1] = True
    
    for i in range(m):
        for j in range(n):
            if p[j] == '*': 
                dp[i + 1][j + 1] = dp[i + 1][j - 1] | ((p[j - 1] == s[i] or p[j - 1] == '.') and dp[i][j + 1])
            else:
                (p[j] == s[j] or p[j] == '.') and dp[i + 1][j + 1] == dp[i][j]
    
    return dp[-1][-1]

assert wildcardMatch('aa', 'a') == False
assert wildcardMatch('aa', 'a*') == True
assert wildcardMatch('ab', '.*') == True

# ===== END FILE: Confluent/wildcardMatch-1.py =====

# ===== BEGIN FILE: Confluent/wildcardMatch-2.py =====

"""
Given an input string s and a pattern p, implement wildcard matching with these rules:
p contains only lowercase/uppercase letters and optionally one *.
There is no ? in the pattern.
* (if present) matches any sequence of characters, including the empty sequence.
The match must cover the entire string s (not partial).
Return True if p matches s, otherwise False.

Examples
s="aa", p="a" → False
s="aa", p="*" → True
s="abcd", p="ab*cd" → True
s="abcd", p="ab*ce" → False
s="abcd", p="*cd" → True
s="abcd", p="ab*" → True
"""
# p has zero or one '*'
def matchStr(s, p):
    if '*' not in p:
        return s == p
    
    left, right = p.split('*')
    if len(s) < len(left) + len(right):
        return False 
    
    return s.startswith(left) and s.endswith(right)

assert matchStr("","") == True
assert matchStr("","a") == False
assert matchStr("aa","") == False
assert matchStr("aa","a") == False
assert matchStr("aa","*") == True
assert matchStr("abcd", "ab*cd") == True
assert matchStr("abcd","ab*ce") == False
assert matchStr("abcd","*cd") == True
assert matchStr("abcd", "ab*") == True
assert matchStr("a", "a*a") == False


"""
You are given an input string s and a pattern p.
p contains letters and zero, one, or many * characters.
There is no ?.
* matches any sequence of characters, including empty.
Matching must cover the entire string s.
Implement is_match(s, p) -> bool.

Examples
s="aa", p="*" → True
s="abcd", p="a*d" → True
s="abcd", p="a**c*d" → True (treat consecutive * like one)
s="abcd", p="a*c" → False
s="", p="**" → True
"""
# p has 0 - n '*' 
def matchStr2(s, p):
    if '*' not in p:
        return s == p 

    parts = p.split('*')
    parts = [p for p in parts if p != '']

    startWithStar = p[0] == '*'
    endWithStar = p[-1] == '*'

    # use two pointer match s and p
    i = 0

    if not startWithStar and parts:
        if not s.startswith(parts[0]):
            return False
        i = len(parts[0])
        parts = parts[1:]

    last = None
    if not endWithStar and parts:
        last = parts[-1]
        parts = parts[:-1]
    
    
    # match all middle part
    for p in parts:
        tmp = s.find(p, i)
        if tmp == -1:
            return False
        i = tmp + len(p)
    
    # if exist tail, need match
    if last:
        lastStartIndex = len(s) - len(last)
        
        # tail of s is shorter than tail of p
        if i > lastStartIndex:
            return False
        
        return s.endswith(last)
    return True
        
    
    

# Empty / exact cases
assert matchStr2("", "") == True
assert matchStr2("", "a") == False
assert matchStr2("", "*") == True
assert matchStr2("", "**") == True
assert matchStr2("aa", "") == False
assert matchStr2("aa", "aa") == True
assert matchStr2("aa", "a") == False

# Single '*'
assert matchStr2("aa", "*") == True
assert matchStr2("aa", "a*") == True
assert matchStr2("aa", "*a") == True
assert matchStr2("ab", "a*b") == True          # '*' empty
assert matchStr2("abcd", "ab*cd") == True
assert matchStr2("abcd", "ab*ce") == False
assert matchStr2("abcd", "*cd") == True
assert matchStr2("abcd", "*ce") == False
assert matchStr2("abcd", "ab*") == True
assert matchStr2("abcd", "ac*") == False
assert matchStr2("a", "a*a") == False          # important length corner
assert matchStr2("aba", "a*a") == True
assert matchStr2("ab", "a*a") == False

# Many '*' (including consecutive)
assert matchStr2("abcd", "**") == True
assert matchStr2("abcd", "a**d") == True
assert matchStr2("abcd", "a***d") == True
assert matchStr2("abcd", "***ab***cd***") == True
assert matchStr2("abcd", "***ab***ce***") == False

# Ordered chunks with multiple '*'
assert matchStr2("abcd", "a*b*c*d") == True
assert matchStr2("abcd", "a*b*d") == True
assert matchStr2("abcd", "a*d*c") == False     # wrong order
assert matchStr2("abcd", "*a*b*c*d*") == True
assert matchStr2("abcd", "*a*c*b*") == False   # wrong order

# Prefix/suffix anchoring
assert matchStr2("zzzabc", "abc*") == False
assert matchStr2("abczzz", "abc*") == True
assert matchStr2("zzzabc", "*abc") == True
assert matchStr2("zzzabczzz", "*abc") == False

# Overlap / tight length
assert matchStr2("aaaaa", "aa*aa") == True
assert matchStr2("aaa", "aa*aa") == False
assert matchStr2("ababa", "ab*aba") == True
assert matchStr2("ababa", "aba*aba") == False

# Middle contains
assert matchStr2("abc", "*b*") == True
assert matchStr2("ac", "*b*") == False
assert matchStr2("abc", "**b**") == True

# Case sensitivity
assert matchStr2("Abc", "A*") == True
assert matchStr2("Abc", "a*") == False


# ===== END FILE: Confluent/wildcardMatch-2.py =====

# ===== BEGIN FILE: EA GAMES/buildServer.py =====

"""
Coding test:
backend:
# The Challenge: Service Catalog Microservice # You are tasked with building the core of a new Service Catalog API. This API must manage a list of infrastructure services for the PI&E organization. 

# ### Setup & Data Model 

# Define a Go struct named Service to hold the following fields. Ensure appropriate JSON tags are used for marshaling/unmarshaling: # ID (string) # Name (string) # Owner (string) # Status (string) # Initialize an In-Memory Store: Create a global slice or map to store the Service objects in memory. Populate it with this initial data: # Go # {ID: "S101", Name: "Managed K8s Cluster", Owner: "Infra Team", Status: "Available"}, # {ID: "S102", Name: "S3 Storage Bucket", Owner: "Data Team", Status: "Available"}, # {ID: "S103", Name: "Internal Metrics Dashboard", Owner: "Observability", Status: "Deprecated"} # 

### Implement Endpoints # Set up a basic HTTP server using Go's built-in net/http package or a simple framework (e.g., Gin/Echo). 

Implement the following two REST endpoints: 

# #### GET /api/services: # Return the entire list of services in JSON format. # Must respond with HTTP Status 200 OK. 

# #### POST /api/services: # Accept a JSON body representing a new service request (requiring only Name and Owner). 

# Assign a new, unique ID to the service (e.g., auto-incrementing counter or UUID). 

# Set the initial Status to "In Progress".

# Add the new service to the in-memory store. # Must respond with HTTP Status 201 Created. 

# ## Verification 

# Start the Go server in the terminal. # Use the curl command in the same terminal to verify both the GET and POST endpoints are working as expected. 


frontend:

# The Challenge: 

Data Consumption and Table View You are tasked with building a component to consume and display service status data for the Service Catalog frontend. 

### Data Model & Fetching Define a TypeScript interface (or type) to model the data returned from the public API: https://jsonplaceholder.typicode.com/todos. 

Hint: The key fields are id, title, and completed. Create a component (e.g., ServiceStatusTable). Fetch Data: Use a fetch or axios call within useEffect to retrieve the data from the public endpoint. 

### UI Implementation Table Rendering: Display the fetched data in a visually clear HTML table with three columns: Service ID (mapped from id) Service Name (mapped from title) Provisioning Status (mapped from completed): If completed is true, show the status as "Available". 

If completed is false, show the status as "In Progress". State Handling: Implement the following states using React hooks: Loading State: Show a simple "Loading services..." message while the data is being fetched. Error State: If the fetch fails, display a clear "Error loading data." message. 

## Verification Run the React app (e.g., npm start in the terminal). Verify the browser view shows the table with data correctly mapped and transformed.
"""

import json
# asdict converts a dataclass instance into a plain python dict recursively - perfect for JSON
from dataclasses import dataclass, asdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, List, Any


# -----------------------------
# 1) Data Model: Service
# -----------------------------
@dataclass
class Service:
    id: str
    name: str
    owner: str
    status: str

    def toJsonDict(self):
        return asdict(self)
    

# -----------------------------
# 2) In-Memory Store (global)
# -----------------------------
# Initialize an in-memory store and pre-populate it with initial data
serviceStore: Dict[str, Service] = {
    "S101": Service(id="S101", name="Managed K8s Cluster", owner="Infra Team", status="Available"),
    "S102": Service(id="S102", name="S3 Storage Bucket", owner="Data Team", status="Available"),
    "S103": Service(id="S103", name="Internal Metrics Dashboard", owner="Observability", status="Deprecated"),  
}

nextIdNumber = 104
# Assign a new unique ID to each new service(auto-incrementing)
def generateNextId():
    global nextIdNumber
    newId = f"S{nextIdNumber}"
    nextIdNumber += 1
    return newId


# -----------------------------
# 3) HTTP Handler + Endpoints
# -----------------------------
class Handler(BaseHTTPRequestHandler):
    def sendJson(self, statusCode, payload):
        # helper to return JSON with correct HTTP status
        # json.dumps: take a python object, convert it into a JSON string
        # encode('utf-8') converts string into bytes
        bodyBytes = json.dumps(payload).encode('utf-8')
        self.send_response(statusCode)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(bodyBytes)))
        self.end_headers()
        self.wfile.write(bodyBytes)

    def readJsonBody(self) -> Dict[str, Any]:
        contentLength = int(self.headers.get('Content-Length', '0'))
        rawBytes = self.rfile.read(contentLength) if contentLength > 0 else b''
        if not rawBytes:
            return {}
        # convert json str into python obj(dict)
        return json.loads(rawBytes.decode('utf-8'))
    def do_GET(self):
        # Req: GET /api/services returns the entire list, http 200
        if self.path != '/api/services':
            self.sendJson(404, {'error': 'Not found'})
            return
        # svc.toJsonDict()
        # converts each service object into a plain python dict with JSON-friendly keys
        serviceJson = [svc.toJsonDict() for svc in serviceStore.values()]
        self.sendJson(200, serviceJson)
    
    def do_POST(self):
        # Req POST /api/services accepts Name + Owner, creates new service, http 201
        if self.path != '/api/services':
            self.sendJson(404, {'error': 'Not found'})
            return 
        
        try:
            data = self.readJsonBody()
        except Exception:
            self.sendJson(400, { 'error': 'Invalid JSON body'})
            return 
        
        # request requires only name and owner
        name = data.get("Name") or data.get("name")
        owner = data.get("Owner") or data.get("owner")

        name = (name or '').strip()
        owner = (owner or '').strip()

        if not name or not owner:
            self.sendJson(400, {'error': "Body must include non-empty 'Name' and 'Owner'"})
            return
        
        # Req: assign unique ID and set status to 'in progress'
        newId = generateNextId()
        newService = Service(
            id = newId,
            name = name.strip(),
            owner = owner.strip(),
            status="In Progress",
        )

        # Req: add to in-memory store
        serviceStore[newId] = newService

        # Req: respond HTTP 201 created with created service JSON
        self.sendJson(201, newService.toJsonDict())

def runServer(host: str = '0.0.0.0', port: int = 8000):
    httpd = HTTPServer((host, port), Handler)
    print(f"Service Catalog API running on http://{host}:{port}")
    print("Try: GET  /api/services")
    print("Try: POST /api/services  body: {\"Name\":\"Redis Cache\",\"Owner\":\"Platform Team\"}")
    
    httpd.serve_forever()

runServer()


# frontend


# ===== END FILE: EA GAMES/buildServer.py =====

# ===== BEGIN FILE: Google/FindMedianInLargeArray.py =====

"""
(This question is a variation of the LeetCode question 295. Find Median from Data Stream. 
If you haven't completed that question yet, it is recommended to solve it first.)

In the world of big data, analysts often work with massive, unsorted datasets. 
Imagine you are given a very large and unsorted array of integers nums. 
Your task is to develop an efficient method to find its median.

The median is the middle value in an ordered dataset, which is defined as:

If the array contains an odd number of elements, the median is the single middle 
element after sorting. If the array contains an even number of elements, the median 
is the average of the two middle elements after sorting. Since the array can be 
extremely large, your solution must run in the time complexity of amortized 
O(N)

Constraints:
1 ≤ nums.length ≤ 10^5
-2^31 <= nums[i] < 2^31 - 1
"""
from collections import defaultdict
import heapq
class Solution:
    def __init__(self):
        self.left = []
        self.right = []
    
    # move max value in left to right
    def L2R(self):
        t = heapq.heappop(self.left)
        heapq.heappush(self.right, -t)

    # move min value in right to left
    def R2L(self):
        t = heapq.heappop(self.right)
        heapq.heappush(self.left, -t)

    def findMedian(self, nums):
        # principle: left num 
        # for each num, put into left first
        # then pop out the max num from left, move it into right
        for num in nums:
            heapq.heappush(self.left, -num)

            t = heapq.heappop(self.left)
            heapq.heappush(self.right, -t)

            if len(self.right) > len(self.left) + 1:
                self.R2L()
        
        if len(self.right) == len(self.left) + 1:
            return float(self.right[0])
        else:
            return (self.right[0] - self.left[0]) / 2


def runTests():
    # 1) Single element
    s = Solution()
    assert s.findMedian([5]) == 5

    # 2) Odd count, unsorted
    s = Solution()
    assert s.findMedian([3, 1, 2]) == 2

    # 3) Even count, unsorted
    s = Solution()
    assert s.findMedian([4, 1, 2, 3]) == 2.5  # sorted: [1,2,3,4]

    # 4) With duplicates
    s = Solution()
    assert s.findMedian([2, 2, 2, 2]) == 2.0

    # 5) Negative numbers
    s = Solution()
    assert s.findMedian([-5, -1, -3]) == -3  # sorted: [-5,-3,-1]

    # 6) Mix negative and positive, even count
    s = Solution()
    assert s.findMedian([-1, 0, 1, 2]) == 0.5  # sorted: [-1,0,1,2]

    # 7) Large extremes (32-bit bounds style)
    s = Solution()
    assert s.findMedian([-(2**31), 2**31 - 1]) == (-1) / 2  # -0.5

    # 8) Already sorted increasing
    s = Solution()
    assert s.findMedian([1, 2, 3, 4, 5]) == 3

    # 9) Sorted decreasing
    s = Solution()
    assert s.findMedian([5, 4, 3, 2, 1]) == 3

    # 10) Random-ish
    s = Solution()
    assert s.findMedian([10, 7, 2, 3, 5]) == 5  # sorted: [2,3,5,7,10]

    print("All tests passed!")

runTests()


"""
Top 3 most common follow-ups for this median problem:

1 Turn it into a real data stream
Implement addNum(x) and findMedian() (LeetCode 295).
Expect: two heaps, addNum: O(log n), findMedian: O(1).

2 Sliding window median
“Return median for every window of size k” (LeetCode 480).
Expect: two heaps + lazy deletion hash map, O(n log k).

3 Can’t store all data / very large dataset
“Data doesn’t fit memory—how to get median?”
Exact: external-memory selection / multi-pass counting (if bounded range) / distributed selection.
Approx: quantile sketch (e.g., GK / t-digest).
"""

# follow-up 1 Data stream Median
class MedianFinder:
    def __init__(self):
        self.left = []
        self.right = []
    
    def addNum(self, num):
        if not self.right or num >= self.right[0]:
            heapq.heappush(self.right, num)
        else:
            heapq.heappush(self.left, -num)
        
        # rebalance so that right has same count as left, or 1 more
        if len(self.right) > len(self.left) + 1:
            heapq.heappush(self.left, -heapq.heappop(self.right))
        elif len(self.left) > len(self.right):
            heapq.heappush(self.right, -heapq.heappop(self.left))
    
    def findMedian(self):
        if not self.right and not self.left:
            return 0.0
        
        if len(self.right) == len(self.left) + 1:
            return float(self.right[0])
        
        return (self.right[0] - self.left[0]) / 2.0
    
def testMedianFinder():
    mf = MedianFinder()
    for x in [3, 1, 2]:
        mf.addNum(x)
    assert mf.findMedian() == 2.0

    mf = MedianFinder()
    for x in [4, 1, 2, 3]:
        mf.addNum(x)
    assert mf.findMedian() == 2.5

    mf = MedianFinder()
    for x in [-1, 0, 1, 2]:
        mf.addNum(x)
    assert mf.findMedian() == 0.5

testMedianFinder()

# sliding window median
# use lazyHeap
class DualHeap:
    def __init__(self, k):
        self.small = [] # max-heap for smaller part
        self.large = [] # min-heap for larger part
        self.delayed = defaultdict(int) # # record already deleted num
        self.smallSize = 0 # record real size for small
        self.largeSize = 0 # record real size for large
        self.k = k

    # clean deleted num on top
    def _pruneSmall(self):
        while self.small:
            num = -self.small[0]
            if self.delayed[num] > 0:
                heapq.heappop(self.small)
                self.delayed[num] -= 1
            else:
                break
    # clean deleted num on top
    def _pruneLarge(self):
        while self.large:
            num = self.large[0]
            if self.delayed[num] > 0:
                heapq.heappop(self.large)
                self.delayed[num] -= 1
            else:
                break
    # rebalance via compare smallSize and largeSize
    def _makeBalance(self):
        # keep smallSize == largeSize or smallSize == largeSize + 1
        if self.smallSize > self.largeSize + 1:
            val = -heapq.heappop(self.small)
            self.smallSize -= 1
            heapq.heappush(self.large, val)
            self.largeSize += 1
            self._pruneSmall() # prune the new top in small
        elif self.smallSize < self.largeSize:
            val = heapq.heappop(self.large)
            self.largeSize -= 1
            heapq.heappush(self.small, -val)
            self.smallSize += 1
            self._pruneLarge()

    # add new head to heap
    def add(self, num):
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
            self.smallSize += 1
        else:
            heapq.heappush(self.large, num)
            self.largeSize += 1
        self._makeBalance()
        
    # remove old tail of window from heap
    def remove(self, num):
        self.delayed[num] += 1

        if self.small and num <= -self.small[0]:
            self.smallSize -= 1
            if num == -self.small[0]:
                self._pruneSmall()
        else:
            self.largeSize -= 1
            if num == self.large[0]:
                self._pruneLarge()
        
        self._makeBalance()

    def getMedian(self):
        if self.k % 2 == 1:
            return float(-self.small[0])
        return (self.large[0] - self.small[0]) / 2.0


def medianSlidingWindow(nums, k):
    if k <= 0 or not nums or k > len(nums):
        return []
    
    dh = DualHeap(k)
    for i in range(k):
        dh.add(nums[i])
    
    res = [dh.getMedian()]

    for i in range(k, len(nums)):
        dh.add(nums[i])
        dh.remove(nums[i - k])
        res.append(dh.getMedian())
    
    return res
    

def testMedianSlidingWindow():
    assert medianSlidingWindow([1,3,-1,-3,5,3,6,7], 3) == [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
    assert medianSlidingWindow([1,2,3,4], 2) == [1.5, 2.5, 3.5]
    assert medianSlidingWindow([2,2,2,2], 2) == [2.0, 2.0, 2.0]

testMedianSlidingWindow()

"""
3) Too Large to Fit Memory (Exact) — Bounded Value Range
If values are within a known small range [minVal, maxVal], you can compute the median with counts.
Time: O(n + R) where R = maxVal - minVal + 1
Space: O(R) (no need to store all numbers)
"""
def medianFromIteratorBoundedRange(numsIter, minVal, maxVal):
    if minVal > maxVal:
        return 0.0
    
    size = maxVal - minVal + 1
    counts = [0] * size
    total = 0

    for x in numsIter:
        counts[x - minVal] += 1
        total += 1
    
    if total == 0:
        return 0.0
    
    k1 = (total - 1) // 2 # left num for median
    k2 = total // 2   # right num for median

    def findKth(k):
        running = 0
        for i, cnt in enumerate(counts):
            running += cnt
            if running > k:
                return i + minVal
        return maxVal # should never hit
    
    a = findKth(k1)
    b = findKth(k2)
    return (a + b) / 2.0


# ===== END FILE: Google/FindMedianInLargeArray.py =====

# ===== BEGIN FILE: Google/FindWordPathInCubes.py =====

""" 
You are given a word and a set of cubes. Each cube has 6 sides with a letter on each side. 
Spell the word using the cubes and return which cubes you used. Note: 
You cannot use the same cube to spell multiple letters. 
word = "phone" 
cubes = [ 
["h", "r", "y", "q", "t", "y"], 
["r", "m", "o", "f", "a", "r"], 
["r", "m", "p", "f", "a", "f"], 
["y", "z", "x", "n", "a", "b"], 
["g", "p", "z", "e", "m", "n"] 
] 
# Example output: [2, 0, 1, 3, 4]
"""
from collections import defaultdict

def spellWordWithCubes(word, cubes):
    m = len(word)
    n = len(cubes)
    # cube list become cube set help find letter
    cubeSets = [set(c) for c in cubes]

    # letter -> cubes
    wordToCube = defaultdict(list)
    for w in word:
        for idx, cs in enumerate(cubeSets):
            if w in cs:
                wordToCube[w].append(idx)
    
    print('wordToCube', wordToCube)
    
    visitedCube = [-1] * n
    ans = [-1] * m
    # iterate letter in word, find a valid choice for each letter
    def dfs(letterIdx):
        if letterIdx == m:
            return True

        letter = word[letterIdx]
        candidates = wordToCube[letter]

        for cubeIdx in candidates:
            if visitedCube[cubeIdx] != -1:
                continue

            visitedCube[cubeIdx] = 1
            ans[letterIdx] = cubeIdx

            if dfs(letterIdx + 1):
                return True

            visitedCube[cubeIdx] = -1
            ans[letterIdx] = -1
        
        return False
    
    ok = dfs(0)
    return ans if ok else []



# def spellWordWithCubes(word, cubes):
#     n = len(word)
#     m = len(cubes)

#     if n > m:
#         return []
    
#     cubeSets = [set(c) for c in cubes] # O(1) for search in cube

#     options = [] # options[i] means which cubes can supply word[i]
#     for ch in word:
#         candidates = [idx for idx in range(m) if ch in cubeSets[idx]]
#         options.append(candidates)

#     print('options:', options)
    
#     # order = sorted(range(n), key = lambda i: len(options[i]))

#     usedCubes = set()
#     assignment = [-1] * n

#     # first check smallest candidates
#     def backtrack(orderIdx):
#         # reach end condition, find a right choice
#         if orderIdx == n:
#             return True

#         # target letter position in word
#         pos = orderIdx

#         # choose candidate cube for target letter
#         for cubeIdx in options[pos]:
#             # skip already used cube
#             if cubeIdx in usedCubes:
#                 continue

#             # use a cube, add a pos info
#             usedCubes.add(cubeIdx)
#             assignment[pos] = cubeIdx

#             if backtrack(orderIdx + 1):
#                 return True
            
#             # restore the usedCube and pos info
#             usedCubes.remove(cubeIdx)
#             assignment[pos] = -1

#         return False
#     ok = backtrack(0)
#     # time O(m^n) space (n + m)
#     return assignment if ok else []
            
# --- quick test with your sample ---
word = "phone"
cubes = [
    ["h", "r", "y", "q", "t", "y"],  # 0
    ["r", "m", "o", "f", "a", "r"],  # 1
    ["r", "m", "p", "f", "a", "f"],  # 2
    ["y", "z", "x", "n", "a", "b"],  # 3
    ["g", "p", "z", "e", "m", "n"],  # 4
]

print(spellWordWithCubes(word, cubes))  # one valid output: [2, 0, 1, 3, 4]


# ===== END FILE: Google/FindWordPathInCubes.py =====

# ===== BEGIN FILE: Google/LongestMatchTokenization.py =====

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

        



# ===== END FILE: Google/LongestMatchTokenization.py =====

# ===== BEGIN FILE: Google/MaximumIslandPerimeter.py =====

"""
(This question is a variation of the LeetCode question 200. Number of Islands. If you haven't completed that question yet, it is recommended to solve it first.)

You are given a matrix grid of size m x n where each element is either land ('1') or water ('0'). A group of connected '1's (land) forms an island. Two land cells are considered connected if they are adjacent vertically or horizontally (not diagonally).

Each land cell has up to four edges. An edge contributes to the island's perimeter if it is either adjacent to water or lies on the boundary of the matrix.

Return the maximum perimeter among all islands in the grid. If there is no island, return 0.

Constraints:

1 ≤ m ≤ 100
1 ≤ n ≤ 100
Each grid[i][j] is either '0'(water) or '1'(land)
"""
# time O(m * n) space O(m * n)
def maxPerimeter(g):
    m, n = len(g), len(g[0])
    visited = [[0] * n for _ in range(m)]
    DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    # 
    def dfs(x, y):
        cnt = 0
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            # go grid outside
            if not (0 <= nx < m and 0 <= ny < n):
                cnt += 1
            # border of island
            elif g[nx][ny] == '0':
                cnt += 1
            elif visited[nx][ny] == 0:
                visited[nx][ny] = 1
                cnt += dfs(nx, ny)
        return cnt
    res = 0
    for x in range(m):
        for y in range(n):
            if visited[x][y] == 0 and g[x][y] == '1':
                visited[x][y] = 1
                cnt = dfs(x, y)
                res = max(res, cnt)
                
    return res

 # 1) No land
grid1 = [["0"]]
assert maxPerimeter(grid1) == 0

# 2) Single land cell
grid2 = [["1"]]
assert maxPerimeter(grid2) == 4

# 3) One island: 2x2 block -> perimeter 8
grid3 = [
    ["1", "1"],
    ["1", "1"],
]
assert maxPerimeter(grid3) == 8

# 4) Two separate single-cell islands -> max perimeter 4
grid4 = [
    ["1", "0", "1"],
]
assert maxPerimeter(grid4) == 4

# 5) L-shape island -> perimeter 8
# 1 1
# 1 0
grid5 = [
    ["1", "1"],
    ["1", "0"],
]
assert maxPerimeter(grid5) == 8

# 6) Two islands: (line of 3) perimeter 8, (single) perimeter 4 => max 8
grid6 = [
    ["1", "1", "1", "0"],
    ["0", "0", "0", "1"],
]
assert maxPerimeter(grid6) == 8

# 7) Complex: max should come from the big island
grid7 = [
    ["0","1","0","0","0"],
    ["1","1","1","0","0"],
    ["0","1","0","0","1"],
    ["0","0","0","1","1"],
]
# Island A is plus-shape-like (5 cells) perimeter = 12
# Island B is 3 cells connected (an L) perimeter = 8
assert maxPerimeter(grid7) == 12

print("All tests passed!")

# Uncomment to run locally:
# runTests()




# ===== END FILE: Google/MaximumIslandPerimeter.py =====

# ===== BEGIN FILE: Google/TollCheckpoint.py =====

"""
Toll Checkpoint Billing
A highway has multiple toll checkpoints. Each time a vehicle passes a checkpoint, 
the system records a log entry containing:
license plate
checkpoint name
timestamp

The checkpoint name is an alphanumeric string like "A1", "C7", "D10".
Its numeric part represents the checkpoint position on the highway.

Toll fee rule
The toll fee for traveling between two checkpoints is calculated by taking the absolute difference 
between their positions and multiplying it by 10 (excluding any characters). 
For example, the toll fee for a vehicle passing through checkpoints "A1" and "A5" is calculated as |1 - 5| * 10 = 40.
"""
from collections import defaultdict

def getTrailingNumber(s):
    i = len(s) - 1
    while i >= 0 and s[i].isdigit():
        i -= 1
    return int(s[i + 1:])

def calculateFee(logEntries):
    carLog = defaultdict(list)
    logs = [item.split(',') for item in logEntries]
    for car, position, timestamp in logs:
        p = getTrailingNumber(position)
        carLog[car].append([int(timestamp), p])
    
    fees = defaultdict(int)

    for k, vs in carLog.items():
        vs.sort()
        startTime, startP = vs[0]
        for t, p in vs[1:]:
            if t > startTime:
                fees[k] += abs(p - startP) * 10
            startTime = t 
            startP = p

    return [f'License: {k}, Fee: {v}' for k, v in fees.items()]



def runTests():
    tests = [
        # Example 1
        (
            ["CAR123,A1,1000", "CAR123,A5,2000"],
            ["License: CAR123, Fee: 40"],
        ),

        # Example 2 (order of results can vary, so we compare as sets)
        (
            ["CAR111,C2,1100", "CAR111,C4,1300",
             "CAR222,C1,1000", "CAR222,C3,1500", "CAR222,C7,2000"],
            ["License: CAR111, Fee: 20", "License: CAR222, Fee: 60"],
        ),

        # Example 3
        (
            ["CAR999,D10,3000", "CAR999,D1,1000", "CAR999,D5,2000"],
            ["License: CAR999, Fee: 90"],
        ),

        # Interleaved multi-cars, out-of-order logs
        (
            ["A,A4,1500", "B,B2,1200", "A,A1,1000", "B,B5,1000", "B,B9,2000"],
            ["License: A, Fee: 30", "License: B, Fee: 100"],
        ),

        # Repeated checkpoint => 0 segment
        (
            ["CAR1,A3,1000", "CAR1,A3,2000", "CAR1,A8,3000"],
            ["License: CAR1, Fee: 50"],
        ),

        # Same timestamp (your code ignores hops where t == startTime)
        (
            ["T1,X1,1000", "T1,X10,1000", "T1,X5,2000"],
            ["License: T1, Fee: 50"],
        ),

        # Multi-digit positions
        (
            ["CAR2,Z10,1000", "CAR2,Z2,2000", "CAR2,Z15,3000"],
            ["License: CAR2, Fee: 210"],
        ),
    ]

    for i, (logs, expected) in enumerate(tests, 1):
        got = calculateFee(logs)
        assert set(got) == set(expected), f"Test {i} failed.\nExpected: {expected}\nGot: {got}"

    print("All tests passed!")


if __name__ == "__main__":
    runTests()

# ===== END FILE: Google/TollCheckpoint.py =====

# ===== BEGIN FILE: Google/URLRouterDesign.py =====

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

# ===== END FILE: Google/URLRouterDesign.py =====

# ===== BEGIN FILE: Google/WindowedAverageexcludingLargestK.py =====

"""
Sliding Window Averages Ignoring Top-k

You are given:
an integer array nums
an integer windowSize
an integer k

For every contiguous subarray (sliding window) of length windowSize, compute the average of the window after removing
(ignoring) the largest k values in that window.

Return a list ans where:
ans[i] is the average for the window nums[i : i + windowSize] after ignoring its largest k numbers.

Notes
“Ignore the largest k numbers” means: remove exactly k elements with the greatest values in the window 
(if there are duplicates, remove any k of them).
"""
from sortedcontainers import SortedList
# a window with s size
# use sortedDict to contain all num in window
# after each update 
def slidingWindowAvg(nums, windowSize, k):
    result = []
    if nums is None or len(nums) < windowSize or k < 0 or k >= windowSize:
        return result
    
    n = len(nums)
    
    window = SortedList(nums[:windowSize])
    windowSum = sum(nums[:windowSize])
    keepCnt = windowSize - k 

    def topKSum():
        s = 0
        for i in range(1, k + 1):
            s += window[-i]
        return s
    
    # init ans 
    ans = [(windowSum - topKSum()) / keepCnt]

    for r in range(windowSize, n):
        oldV = nums[r - windowSize]
        inV = nums[r]

        window.remove(oldV) # remove old num out
        window.add(inV)  # add new num into sortedlist
        windowSum += inV - oldV # update sum of window

        ans.append((windowSum - topKSum()) / keepCnt)
    # time O(n(logw + k)) space O(w)
    return ans

    

# ===== END FILE: Google/WindowedAverageexcludingLargestK.py =====

# ===== BEGIN FILE: Rivian/numberToWords.py =====

"""
Description

Your task is to write a function that converts a non-negative integer into its spoken word (English) equivalent.

Examples
fn(7)      => "seven"
fn(77)     => "seventy-seven"
fn(777)    => "seven hundred and seventy-seven"
fn(7777)   => "seven thousand seven hundred and seventy-seven"
fn(54321)  => "fifty-four thousand three hundred and twenty-one"

Rules & Notes

Numbers should be written in British English style, using:

hyphens for compound numbers (twenty-one, seventy-seven)

the word "and" between hundreds and tens/ones
(e.g. "three hundred and five")

Scale words include:

hundred

thousand

(and potentially higher if extended)

No trailing or leading spaces.

Output should be a single string.
"""

# 1 to 9 billion
# def numberToWords(num):
#     specials = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(" ")
#     tens = "twenty thirty forty fifty sixty seventy eighty ninety".split(" ")
#     hundred = "hundred"
#     thousand = "thousand"
#     million = "million"
#     billion = "billion"

#     if num < 20:
#         return specials[num]
#     if num < 100:
#         if num % 10 == 0:
#             return tens[num // 10 - 2]
#         return tens[num // 10 - 2] + "-" + numberToWords(num % 10)
#     if num < 1000:
#         if num % 100 == 0:
#             return numberToWords(num // 100) + " " + hundred
#         return  numberToWords(num // 100) + " " + hundred + " and " + numberToWords(num % 100)
#     if num < 1000000:
#         if num % 1000 == 0:
#             return numberToWords(num // 1000) + " " + thousand
#         return  numberToWords(num // 1000) + " " + thousand + " " + numberToWords(num % 1000)
#     if num < 1000000000:
#         if num % 1000000 == 0:
#             return numberToWords(num // 1000000) + " " + million
#         return  numberToWords(num // 1000000) + " " + million + " " + numberToWords(num % 1000000)

def numberToWords(num):
    specials = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(" ")
    tens = 'twenty thirty forty fifty sixty seventy eighty ninety'.split(' ')
    hundred = 'hundred'
    thousand = 'thousand'
    million = 'million'
    billion = 'billion'
    if num == 0:
        return 'zero'

    if num < 20: # [0, 20)
        return specials[num]
    if num < 100: # [20, 100)
        if num % 10 == 0:
            return tens[(num // 10) - 2]
        return tens[(num // 10) - 2] + '-' + numberToWords(num % 10)
    if num < 1000: # [100, 1000)
        if num % 100 == 0:
            return numberToWords(num // 100) + ' ' + hundred
        return numberToWords(num // 100) + ' ' + hundred + ' and ' + numberToWords(num % 100)
    if num < 1000000: # [1000, 1 million)
        if num % 1000 == 0:
            return numberToWords(num // 1000) + ' ' + thousand
        return numberToWords(num // 1000) + ' ' + thousand + ' and ' + numberToWords(num % 1000)
    if num < 1000000000: #[1 million, 1 billion)
        if num % 1000000 == 0:
            return numberToWords(num // 1000000) + ' ' + million
        return numberToWords(num // 1000000) + ' ' + million + ' and ' + numberToWords(num % 1000000)

    if num % 1000000000 == 0:
        return numberToWords(num // 1000000000) + ' ' + billion
    return numberToWords(num // 1000000000) + ' ' + billion + ' and ' + numberToWords(num % 1000000000)


def runTests():
    # 0 / small
    assert numberToWords(0) == "zero"
    assert numberToWords(7) == "seven"
    assert numberToWords(19) == "nineteen"
    assert numberToWords(20) == "twenty"
    assert numberToWords(21) == "twenty-one"
    assert numberToWords(90) == "ninety"
    assert numberToWords(99) == "ninety-nine"

    # hundreds
    assert numberToWords(100) == "one hundred"
    assert numberToWords(101) == "one hundred and one"
    assert numberToWords(110) == "one hundred and ten"
    assert numberToWords(115) == "one hundred and fifteen"
    assert numberToWords(999) == "nine hundred and ninety-nine"

    # thousands (multiples / with remainder)
    assert numberToWords(1000) == "one thousand"
    assert numberToWords(1001) == "one thousand and one"
    assert numberToWords(1010) == "one thousand and ten"
    assert numberToWords(1100) == "one thousand and one hundred"
    assert numberToWords(7777) == "seven thousand and seven hundred and seventy-seven"
    assert numberToWords(54321) == "fifty-four thousand and three hundred and twenty-one"

    # millions
    assert numberToWords(1_000_000) == "one million"
    assert numberToWords(1_000_001) == "one million and one"
    assert numberToWords(1_001_000) == "one million and one thousand"
    assert numberToWords(1_234_567) == "one million and two hundred and thirty-four thousand and five hundred and sixty-seven"

    # billions
    assert numberToWords(1_000_000_000) == "one billion"
    assert numberToWords(1_000_000_001) == "one billion and one"
    assert numberToWords(1_000_001_000) == "one billion and one thousand"
    assert numberToWords(2_147_483_647) == (
        "two billion and one hundred and forty-seven million and "
        "four hundred and eighty-three thousand and six hundred and forty-seven"
    )

    print("All tests passed!")

runTests()


# ===== END FILE: Rivian/numberToWords.py =====

# ===== BEGIN FILE: Robinhood/Top10WordFrequency.py =====

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



# ===== END FILE: Robinhood/Top10WordFrequency.py =====

# ===== BEGIN FILE: Robinhood/candlestick.py =====

"""
Candlestick Aggregation (10-unit intervals)
You receive price updates for one stock as (time, price) pairs. Times are non-negative integers. The pairs may be in any order.
For every 10 time units, build candlestick data for each interval:
Interval start time: t0 = (time // 10) * 10 (bucket [t0, t0+10))

For each interval output:
[t0, maxPrice, minPrice, openPrice, closePrice]
openPrice: price at the earliest time in that interval
closePrice: price at the latest time in that interval
maxPrice: highest price in that interval
minPrice: lowest price in that interval

Missing intervals (gap filling)
If an interval has no prices, but there was a previous interval output, then fill the missing interval
using the previous interval’s closePrice for all fields:
[t0, prevClose, prevClose, prevClose, prevClose]
If there is no previous interval yet (no earlier data), skip leading empty intervals.

Output
Return the candlesticks in increasing order of t0.
"""

from collections import defaultdict
def buildCandles(timePrices):
    if not timePrices:
        return []
    
    buckets = defaultdict(list)
    for t, p in timePrices:
        start = (t // 10) * 10
        buckets[start].append((t, p))
    
    starts = sorted(buckets.keys())
    res = []

    prevClose = None
    curStart = starts[0]

    while True:
        if curStart in buckets:
            ps = buckets[curStart]
            ps.sort()

            openPrice = ps[0][1]
            clostPrice = ps[-1][1]
            maxPrice = max(p for _, p in ps)
            minPrice = min(p for _, p in ps)
            res.append([curStart, maxPrice, minPrice, openPrice, clostPrice])
            prevClose = clostPrice
        else:
            res.append([curStart, prevClose, prevClose, prevClose, prevClose])
        
        if curStart == starts[-1]:
            break

        curStart += 10
    # time O(nlgn) n is length of timePrices
    return res



# T1: given example (unsorted input, with gaps to fill)
timePrices = [[1, 2], [3, 4], [9, 8], [5, 10], [13, 18], [34, 32], [55, 44]]
expected = [
    [0, 10, 2, 2, 8],
    [10, 18, 18, 18, 18],
    [20, 18, 18, 18, 18],
    [30, 32, 32, 32, 32],
    [40, 32, 32, 32, 32],
    [50, 44, 44, 44, 44],
]
assert buildCandles(timePrices) == expected

# T2: two intervals, no gaps
timePrices = [[0, 5], [3, 6], [9, 7], [10, 10], [11, 9], [15, 12], [19, 5]]
expected = [
    [0, 7, 5, 5, 7],
    [10, 12, 5, 10, 5],
]
assert buildCandles(timePrices) == expected

# T3: single point
timePrices = [[0, 10]]
expected = [[0, 10, 10, 10, 10]]
assert buildCandles(timePrices) == expected

# T4: open/close from earliest/latest time in the same bucket (input unsorted)
timePrices = [[8, 100], [1, 50], [9, 70], [2, 60]]
expected = [[0, 100, 50, 50, 70]]
assert buildCandles(timePrices) == expected

# T5: leading empty buckets are skipped (first bucket is 20)
timePrices = [[25, 10]]
expected = [[20, 10, 10, 10, 10]]
assert buildCandles(timePrices) == expected

# T6: multiple missing buckets filled with previous close
timePrices = [[1, 5], [41, 7]]
expected = [
    [0, 5, 5, 5, 5],
    [10, 5, 5, 5, 5],
    [20, 5, 5, 5, 5],
    [30, 5, 5, 5, 5],
    [40, 7, 7, 7, 7],
]
assert buildCandles(timePrices) == expected

# T7: boundary between buckets (9 in bucket 0, 10 in bucket 10)
timePrices = [[9, 1], [10, 2]]
expected = [
    [0, 1, 1, 1, 1],
    [10, 2, 2, 2, 2],
]
assert buildCandles(timePrices) == expected

print("All tests passed!")


# ===== END FILE: Robinhood/candlestick.py =====

# ===== BEGIN FILE: Robinhood/courseSchedule-0.py =====

"""
There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. 
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that 
you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return true if you can finish all courses. Otherwise, return false.


Example 1:
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So it is possible.

Example 2:
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1.
So it is impossible.

Constraints:
1 <= numCourses <= 2000
0 <= prerequisites.length <= 5000
prerequisites[i].length == 2
0 <= ai, bi < numCourses
All the pairs prerequisites[i] are unique.
"""

from collections import defaultdict, deque
def canFinish(n, prerequisites):
    g = defaultdict(list)
    indegree = [0] * n

    for s, e in prerequisites:
        g[s].append(e)
        indegree[e] += 1
    
    # init deque, all point which have 0 indegree
    q = deque([idx for idx, cnt in enumerate(indegree) if cnt == 0])

    while q:
        u = q.popleft()
        for v in g[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)

    return sum(indegree) == 0

testCases = [
    # 1) minimal, no prereq
    (1, [], True),

    # 2) simple valid
    (2, [[1, 0]], True),

    # 3) simple cycle
    (2, [[1, 0], [0, 1]], False),

    # 4) self loop
    (3, [[2, 2]], False),

    # 5) chain (0 -> 1 -> 2 -> 3)
    (4, [[1, 0], [2, 1], [3, 2]], True),

    # 6) diamond DAG: 0->1,0->2,1->3,2->3
    (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True),

    # 7) disconnected components, all acyclic
    (6, [[1, 0], [2, 1], [4, 3]], True),

    # 8) disconnected components, one has cycle
    (6, [[1, 0], [2, 1], [0, 2], [4, 3]], False),

    # 9) bigger cycle length 3
    (5, [[1, 0], [2, 1], [0, 2]], False),

    # 10) multiple prerequisites for one course
    # 3 depends on 1 and 2; 1 depends on 0
    (4, [[1, 0], [3, 1], [3, 2]], True),

    # 11) no prereq but many courses
    (10, [], True),

    # 12) dense-ish acyclic (all edges from smaller to larger)
    (5, [[1,0],[2,0],[3,0],[4,0],[2,1],[3,1],[4,1],[3,2],[4,2],[4,3]], True),
]


for n, p, ans in testCases:
    assert canFinish(n, p) == ans

# ===== END FILE: Robinhood/courseSchedule-0.py =====

# ===== BEGIN FILE: Robinhood/courseSchedule-1.py =====

"""
There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. 
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that
you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return the ordering of courses you should take to finish all courses. If there are many valid answers,
return any of them. If it is impossible to finish all courses, return an empty array.

Example 1:
Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0. So the correct course order is [0,1].

Example 2:
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,2,1,3]
Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. 
Both courses 1 and 2 should be taken after you finished course 0.
So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].

Example 3:
Input: numCourses = 1, prerequisites = []
Output: [0]
"""
from collections import defaultdict, deque
def findOrder(n, p):
    g = defaultdict(list)
    indegree = [0] * n

    for e, s in p:
        g[s].append(e)
        indegree[e] += 1
    ans = [idx for idx, cnt in enumerate(indegree) if cnt == 0]
    q = deque(ans)

    while q:
        u = q.popleft()
        for v in g[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
                ans.append(v)
    
    return ans if sum(indegree) == 0 else []


def isValidOrder(numCourses, prerequisites, order):
    if not order:
        # empty only valid when there is a cycle; caller decides expected
        return False
    if len(order) != numCourses:
        return False
    if set(order) != set(range(numCourses)):
        return False

    pos = {c: i for i, c in enumerate(order)}
    for a, b in prerequisites:  # b must be before a
        if pos[b] > pos[a]:
            return False
    return True


testCases = [
    # 1) minimal
    {"numCourses": 1, "prerequisites": [], "expectEmpty": False},

    # 2) simple chain
    {"numCourses": 2, "prerequisites": [[1, 0]], "expectEmpty": False},

    # 3) multiple prereqs (diamond)
    {"numCourses": 4, "prerequisites": [[1,0],[2,0],[3,1],[3,2]], "expectEmpty": False},

    # 4) longer chain
    {"numCourses": 5, "prerequisites": [[1,0],[2,1],[3,2],[4,3]], "expectEmpty": False},

    # 5) disconnected components
    {"numCourses": 6, "prerequisites": [[1,0],[2,1],[4,3]], "expectEmpty": False},

    # 6) star dependencies: many depend on 0
    {"numCourses": 5, "prerequisites": [[1,0],[2,0],[3,0],[4,0]], "expectEmpty": False},

    # 7) cycle of length 2
    {"numCourses": 2, "prerequisites": [[1,0],[0,1]], "expectEmpty": True},

    # 8) cycle of length 3
    {"numCourses": 3, "prerequisites": [[1,0],[2,1],[0,2]], "expectEmpty": True},

    # 9) cycle inside one component, other component acyclic
    {"numCourses": 6, "prerequisites": [[1,0],[2,1],[0,2],[4,3]], "expectEmpty": True},

    # 10) dense-ish DAG (edges from smaller to larger)
    {"numCourses": 5,
     "prerequisites": [[1,0],[2,0],[3,0],[4,0],[2,1],[3,1],[4,1],[3,2],[4,2],[4,3]],
     "expectEmpty": False},
]


# Example how to run (assuming your function is findOrder)
def runTests(findOrder):
    for i, t in enumerate(testCases, 1):
        n, pre, expectEmpty = t["numCourses"], t["prerequisites"], t["expectEmpty"]
        order = findOrder(n, pre)

        if expectEmpty:
            assert order == [], f"Test {i} FAILED: expected [], got {order}"
        else:
            assert isValidOrder(n, pre, order), f"Test {i} FAILED: invalid order {order}"
    print("All tests passed!")

runTests(findOrder)

# ===== END FILE: Robinhood/courseSchedule-1.py =====

# ===== BEGIN FILE: Robinhood/courseSchedule-2.py =====

"""
## Question 1 — Find Middle Course in a Chain

You are given an array `pairs`, where each element is `[pre, course]`, meaning **`pre` must be taken before `course`**.

**Guarantees**

* The pairs form **one single continuous chain** (no branches, no merges).
* The total number of courses in the chain is **odd**.
* Each course appears **at most once** as a prerequisite (except the start) and **at most once** as a course (except the end).

**Task**
Reconstruct the chain and return the **middle course**.

**Example**

* Input: `[["Chemistry","Biology"],["Biology","ComputerScience"],["Math","Physics"],["Physics","Chemistry"]]`
* Chain: `Math -> Physics -> Chemistry -> Biology -> ComputerScience`
* Output: `"Chemistry"`

---

## Follow-up — Find Middle Course of the Longest Path in a DAG

Now `pairs` may form a **Directed Acyclic Graph (DAG)** (still `[pre, course]`).

A **source** course has **no prerequisites** (in-degree = 0).
A **sink** course has **no subsequent courses** (out-degree = 0).

**Task**

1. Consider all paths from any **source** to any **sink**.
2. Find the **unique longest path**.
3. Return the **middle course** on that longest path:

   * If the path length is odd → return the exact middle.
   * If the path length is even → return the middle **closer to the start**
     (e.g., 10 courses → return the 5th course, not the 6th).

**Guarantees**

* The input is a DAG (no cycles).
* There may be multiple sources and sinks.
* The **longest path is unique**.

**Example**

* Input: `[["A","B"],["A","C"],["B","D"],["D","E"],["C","F"]]`
* Longest path: `A -> B -> D -> E` (4 courses, even)
* Middle closer to start = `"B"`
"""

from collections import defaultdict, deque
def middleCourseInChain(pairs):
    nxt = {}
    indeg = defaultdict(int)
    nodes = set()

    for pre, course in pairs:
        nxt[pre] = course
        indeg[course] += 1
        nodes.add(pre)
        nodes.add(course)
    

    start = [x for x in nodes if indeg[x] == 0][0]

    chain = []
    cur = start
    while cur is not None:
        chain.append(cur)
        cur = nxt.get(cur)
    
    return chain[len(chain) // 2]

def middleCourseOfLongestPathDAG(pairs):
    g = defaultdict(list)
    indeg = defaultdict(int)
    nodes = set()

    for u, v in pairs:
        g[u].append(v)
        indeg[v] += 1
        nodes.add(u)
        nodes.add(v)

    q = deque([x for x in nodes if indeg[x] == 0])

    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    dpLen = {u: 1 for u in nodes}
    parent = {u: None for u in nodes}

    for u in topo:
        for v in g[u]:
            if dpLen[u] + 1 > dpLen[v]:
                dpLen[v] = dpLen[u] + 1
                parent[v] = u
    
    end = max(nodes, key = lambda x: dpLen[x])

    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    return path[(len(path) - 1) // 2]

    # ---------- Tests for Q1: single chain, odd length ----------
pairs = [["Chemistry", "Biology"], ["Biology", "ComputerScience"], ["Math", "Physics"], ["Physics", "Chemistry"]]
assert middleCourseInChain(pairs) == "Chemistry"  # Math->Physics->Chemistry->Biology->ComputerScience

pairs = [["Intro", "Data"], ["Data", "Algo"], ["Algo", "Systems"], ["Systems", "AI"], ["AI", "ML"]]
assert middleCourseInChain(pairs) == "Systems"  # Intro->Data->Algo->Systems->AI->ML (len=6?) actually 6 even, so not valid for Q1

pairs = [["Math", "Physics"], ["Physics", "Chemistry"]]
assert middleCourseInChain(pairs) == "Physics"  # Math->Physics->Chemistry


# ---------- Tests for Follow-up: longest path in DAG (unique) ----------
pairs = [["A", "B"], ["A", "C"], ["B", "D"], ["D", "E"], ["C", "F"]]
assert middleCourseOfLongestPathDAG(pairs) == "B"  # longest: A->B->D->E, mid closer start = B

pairs = [["K", "L"], ["L", "M"], ["M", "N"], ["K", "O"], ["O", "P"]]
assert middleCourseOfLongestPathDAG(pairs) == "L"  # longest: K->L->M->N (len=4), mid = L

pairs = [["M", "N"], ["N", "O"], ["O", "P"], ["P", "Q"], ["M", "R"], ["R", "S"], ["X", "Y"], ["Y", "Z"], ["Z", "M"]]
# longest: X->Y->Z->M->N->O->P->Q (len=8), mid closer start = index 3 -> M
assert middleCourseOfLongestPathDAG(pairs) == "M"

print("All tests passed!")


# ===== END FILE: Robinhood/courseSchedule-2.py =====

# ===== BEGIN FILE: Robinhood/employeeReferSystem.py =====

"""
Referral Leaderboard
You are given two arrays of equal length:
referrers[i] — the user who made a referral
referrals[i] — the user who was referred
Each pair represents a referral made in order.
A referral creates a chain. If A → B → C, then A is considered to have referred both B and C.

Rules
A user can be referred only once.
Once a user is on the platform, they cannot be referred again.
Ignore invalid referral events.

Task
For each user, compute their total referral count, including all direct and indirect referrals.
Return a leaderboard of at most 3 users:
Only include users with at least 1 referral
Sort by referral count descending
Break ties by alphabetical order

Output format: "user count"

Example
Input:
referrers = ["A", "B", "C"]
referrals = ["B", "C", "D"]

Output:
["A 3", "B 2", "C 1"]
"""

from collections import defaultdict, deque
def referSystem(referrers, referrals):
    g = defaultdict(list) # each node can have one or many children
    rg = defaultdict(int) # each node have only one parent
    nodes = set() # record all nodes show, all these nodes can not be referred any more

    # time O(n) space O(V + E)
    for u, v in zip(referrers, referrals):
        nodes.add(u)
        if v in nodes: # if already in platform, cannot be referred no more
            continue
        rg[v] = u
        g[u].append(v)
        nodes.add(v)

    outDegree =  { x: len(g[x]) for x in nodes }
    cnt = defaultdict(int)
    

    q = deque()
    # put all outdegree of 0 points into q
    for x in nodes:
        if outDegree[x] == 0:
            q.append(x)

    # time O(V + E) space: O(V)
    while q:
        x = q.popleft()
        if x in rg: # x has parent
            p = rg[x]
            cnt[p] += 1 + cnt[x] # add children's cnt to parent's cnt
            outDegree[p] -= 1 # decrease parent's outdegree
            if outDegree[p] == 0: # if p already be added all children's cnt, add p into queue
                q.append(p)
    
    items = [(u, c) for u, c in cnt.items() if c > 0]
    # time: O(VlogV)
    items.sort(key = lambda t: (-t[1], t[0])) # sort by count decrease, then sort by name increase

    return items[:3]  # time O(n + VlogV) space O(V + E)





        
    

# ===== END FILE: Robinhood/employeeReferSystem.py =====

# ===== BEGIN FILE: Robinhood/findMaximumTrade.py =====

"""
source:
https://www.hack2hire.com/companies/robinhood/coding-questions/67e4c55150b60b77022f3867/practice?questionId=67e8af3a7131f7c901ffd7a1

You are given a list of order records for a single stock. Each record is a list containing the limit price (a number),
quantity (number of shares), and order type (either "buy" or "sell").
Your task is to calculate the total number of shares traded based on the following rules:

A buy order can be matched with a sell order if the sell price is less than or equal to the buy price.
A sell order can be matched with a buy order if the buy price is greater than or equal to the sell price.
If no matching order exists, the order is stored until a matching counter-order arrives.
Orders must be matched at the best possible price:
Buy orders match with the lowest sell price available.
Sell orders match with the highest buy price available.
Orders may be partially filled if the available quantity is less than the order's quantity.
Return the total number of shares successfully traded.

Example 1:
Input: orders = [["150", "5", "buy"],["190", "1", "sell"],["200", "1", "sell"],["100", "9", "buy"],["140", "8", "sell"],["210", "4", "buy"]]
Output: 9
Explanation: There's no trade in the first four orders. Trading begins with the fifth order, a sell at 140 for 8 shares,
which matches a stored buy order at 150, executing 5 shares. The sixth order, a buy at 210 for 4 shares, then triggers 
trading by matching the remaining 3 shares from the sell at 140 and 1 share from the sell at 190. In total, 5 + 4 = 9 shares are traded.

Example 2:
Input: orders = [["100","10","buy"],["105","5","buy"],["110","8","buy"]]
Output: 0

Example 3:
Input: orders = [["120","10","buy"],["115","5","sell"],["110","3","sell"]]
Output: 8

"""
import heapq
def findMaxTradeShares(orders):
    # maintain two books:
    # maxheap for buy order
    # minheap for sell order

    # matching rules
    # incoming buy matches lowest sell while sellPrice <= buyPrice
    # incoming sell matches highest buy while buyPrice >= sellPrice

    bq = [] # buy heap
    sq = [] # sell heap
    res = 0
    
    # time O(nlgn) n is length of order
    # space O(n)
    for price, cnt, type in orders:
        price = int(price)
        cnt = int(cnt)

        if type == 'buy':
            while cnt > 0 and sq and sq[0][0] <= price: # have sell order match
                sellPrice, sellCnt = heapq.heappop(sq)
                m = min(cnt, sellCnt)
                res += m
                cnt -= m
                sellCnt -= m
                if sellCnt > 0:
                    heapq.heappush(sq, (sellPrice, sellCnt))
            
            if cnt > 0:
                heapq.heappush(bq, (-price, cnt))
        
        else: # sell
            while cnt > 0 and bq and -bq[0][0] >= price:
                buyPriceNeg, buyCnt = heapq.heappop(bq)
                m = min(cnt, buyCnt)
                res += m
                cnt -= m
                buyCnt -= m
                if buyCnt > 0:
                    heapq.heappush(bq, (buyPriceNeg, buyCnt))
            
            if cnt > 0:
                heapq.heappush(sq, (price, cnt))
        
    return res


assert findMaxTradeShares([["150","5","buy"],["190","1","sell"],["200","1","sell"],["100","9","buy"],["140","8","sell"],["210","4","buy"]]) == 9
assert findMaxTradeShares([["100","10","buy"],["105","5","buy"],["110","8","buy"]]) == 0
assert findMaxTradeShares([["120","10","buy"],["115","5","sell"],["110","3","sell"]]) == 8



# ===== END FILE: Robinhood/findMaximumTrade.py =====

# ===== BEGIN FILE: Robinhood/fractionalInventory(followup-todo).py =====

"""
## Fractional Shares Inventory (Robinhood)

You are given:
* `orders`: list of orders, each is
  `["SYMBOL", "B" or "S", "QUANTITY", "UNIT_PRICE"]`
* `inventory`: initial fractional inventory, each is
  `["SYMBOL", "FRACTION"]`

All numbers are **integers scaled by 100** (last 2 digits are decimals):
* `"42"` = 0.42
* `"100"` = 1.00
* `UNIT_PRICE` is price per 1 share (scaled by 100)

`QUANTITY` can be:
* a share amount like `"42"` (0.42 shares), or
* a dollar amount like `"$42"` ($0.42), which must be converted to shares using `UNIT_PRICE`.

### Rules (process orders in given order)
For each order on symbol `X`:
* **Buy ("B")**: customer buys shares
  * Use inventory first.
  * If inventory is not enough, Robinhood buys whole shares from the market to cover the shortage and keeps any leftover fractional part in inventory.
* **Sell ("S")**: customer sells shares
  * Add the sold shares into inventory.

After each order, **flatten** inventory for that symbol:
* inventory must be **non-negative**
* inventory must be **< 1.00 share**
(if inventory becomes `>= 1.00`, sell whole shares to the market to reduce it)

### Output
Return the final `inventory` list in the **same order and format** as the input inventory:
`["SYMBOL", "FRACTION"]` (still scaled by 100).

fractional sharing，就是input有些变化，每个order和inventory的元素都变成string，然后内部通过 / 分隔。
"""

# result is real fraction share * 100
def parseQtyToShare100(qty, price100Str):
    if qty.startswith('$'): # qty is money
        dollars100 = int(qty[1:])
        price100 = int(price100Str)
        if price100 == 0:
            return 0
        return (dollars100 * 100) // price100
    return int(qty)

def processOrders(orders, inventory):
    invMap = {}
    invOrder = [sym for sym, _ in inventory]

    for sym, qty in inventory:
        invMap[sym] = int(qty) % 100
    
    for sym, orderType, qty, price100 in orders:
        if sym not in invMap:
            invMap[sym] = 0
        
        qty100 = parseQtyToShare100(qty, price100)

        if orderType == 'B':
            invMap[sym] = (invMap[sym] - qty100) % 100
        else:
            invMap[sym] = (invMap[sym] + qty100) % 100
    
    return [[sym, str(invMap[sym])] for sym in invOrder]


# All-in-one test cases (orders, inventory, expected)
testCases = [
    {
        "name": "T1_buy_from_inventory_only",
        "orders": [["AAPL","B","42","100"]],
        "inventory": [["AAPL","99"]],
        "expected": [["AAPL","57"]],
    },
    {
        "name": "T2_dollar_buy_from_inventory",
        "orders": [["AAPL","B","$42","100"]],
        "inventory": [["AAPL","50"]],
        "expected": [["AAPL","8"]],
    },
    {
        "name": "T3_buy_needs_market_whole_share",
        "orders": [["AAPL","B","50","100"]],
        "inventory": [["AAPL","20"]],
        "expected": [["AAPL","70"]],
    },
    {
        "name": "T4_sell_causes_flatten",
        "orders": [["AAPL","S","75","100"], ["AAPL","S","50","100"]],
        "inventory": [["AAPL","0"]],
        "expected": [["AAPL","25"]],
    },
    {
        "name": "T5_buy_sell_buy_multiple_steps",
        "orders": [["AAPL","B","80","100"], ["AAPL","S","50","100"], ["AAPL","B","10","100"]],
        "inventory": [["AAPL","60"]],
        "expected": [["AAPL","20"]],
    },
    {
        "name": "T6_dollar_buy_non_1_price_exact_division",
        "orders": [["AAPL","B","$100","200"]],  # $1.00 @ $2.00 => 0.50 shares
        "inventory": [["AAPL","10"]],
        "expected": [["AAPL","60"]],
    },
    {
        "name": "T7_multiple_symbols_keep_inventory_order",
        "orders": [["AAPL","B","50","100"], ["GOOG","S","80","100"]],
        "inventory": [["AAPL","30"], ["GOOG","90"]],
        "expected": [["AAPL","80"], ["GOOG","70"]],
    },
    {
        "name": "T8_zero_quantity_noop",
        "orders": [["AAPL","B","0","100"], ["AAPL","S","0","100"]],
        "inventory": [["AAPL","55"]],
        "expected": [["AAPL","55"]],
    },
]



def runTests():
    for t in testCases:
        got = processOrders(t["orders"], t["inventory"])
        assert got == t["expected"], f'{t["name"]} FAILED\n got={got}\n exp={t["expected"]}'
    print("All tests passed!")

runTests()

# ===== END FILE: Robinhood/fractionalInventory(followup-todo).py =====

# ===== BEGIN FILE: Robinhood/friendBalanceTracker.py =====

"""
Social App: Friends + Money Transfers
You are given a list of API requests. Each request is:[seqId, path]
seqId is a unique string like "1", "2", ...
path is one of these:

1) Register
v1/REGISTER/{user}/{initialBalance}
Create a new user with starting balance.

2) Send friend request
v1/FRIEND_REQUEST/{fromUser}/{toUser}
Create a pending friend request.
Store it using this request’s seqId.

3) Accept friend request
v1/ACCEPT_FRIEND/{seqId}
Accept the earlier friend request whose sequence id is seqId.
After acceptance, the two users become friends forever (undirected).

4) Send money
v1/SEND_MONEY/{fromUser}/{toUser}/{amount}
Transfer amount from fromUser to toUser only if:
they are already friends, and
fromUser has at least amount balance
Otherwise, ignore this request.

Task
Process requests in order and return final balances of all users as strings:
"user:balance"
Order of output does not matter.
"""

from collections import defaultdict
from typing import Dict, List, Set, Tuple

def finalBalances(requests):
    balance: Dict[str, int] = {}
    friends: Dict[str, Set[str]] = defaultdict(set) # undirected
    pending: Dict[str, Tuple[str, str]] = {} # seqId -> (fromUser, toUser)

    for seqId, path in requests:
        parts = path.split('/')
        action = parts[1]

        if action == 'REGISTER':
            user = parts[2]
            balance[user] = int(parts[3])
        
        elif action == 'FRIEND_REQUEST':
            fromUser, toUser = parts[2], parts[3]
            pending[seqId] = (fromUser, toUser)
        
        elif action == 'ACCEPT_FRIEND':
            reqId = parts[2]
            if reqId in pending:
                a, b = pending.pop(reqId)
                friends[a].add(b)
                friends[b].add(a)
        
        else:
            fromUser, toUser, amount = parts[2], parts[3], int(parts[-1])

            if toUser in friends[fromUser] and balance.get(fromUser, 0) >= amount:
                balance[fromUser] -= amount
                balance[toUser] = balance.get(toUser, 0) + amount
    # time O(r) r is length of request
    # space O(U + F + P) user count + friendship count + pending count
    return [f'{user}:{bal}' for user, bal in balance.items()]

# T1: sample 1 (friendship required)
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/REGISTER/Charlie/75"],
    ["4", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["5", "v1/ACCEPT_FRIEND/4"],
    ["6", "v1/SEND_MONEY/Alice/Bob/30"],
    ["7", "v1/SEND_MONEY/Charlie/Alice/25"],  # not friends -> ignored
]
expected = sorted(["Alice:70", "Bob:80", "Charlie:75"])
assert sorted(finalBalances(requests)) == expected


# T2: sample 2 (two-way transfers after being friends)
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/REGISTER/Charlie/75"],
    ["4", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["5", "v1/ACCEPT_FRIEND/4"],
    ["6", "v1/SEND_MONEY/Alice/Bob/20"],
    ["7", "v1/SEND_MONEY/Bob/Alice/10"],
]
expected = sorted(["Alice:90", "Bob:60", "Charlie:75"])
assert sorted(finalBalances(requests)) == expected


# T3: sample 3 (send money without friendship -> ignored)
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/SEND_MONEY/Alice/Bob/30"],  # not friends -> ignored
]
expected = sorted(["Alice:100", "Bob:50"])
assert sorted(finalBalances(requests)) == expected


# T4: insufficient balance -> ignored
requests = [
    ["1", "v1/REGISTER/Alice/10"],
    ["2", "v1/REGISTER/Bob/0"],
    ["3", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["4", "v1/ACCEPT_FRIEND/3"],
    ["5", "v1/SEND_MONEY/Alice/Bob/20"],  # Alice has only 10 -> ignored
]
expected = sorted(["Alice:10", "Bob:0"])
assert sorted(finalBalances(requests)) == expected


# T5: accept unknown friend request id -> ignored
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/100"],
    ["3", "v1/ACCEPT_FRIEND/999"],        # no such pending request
    ["4", "v1/SEND_MONEY/Alice/Bob/10"],  # still not friends -> ignored
]
expected = sorted(["Alice:100", "Bob:100"])
assert sorted(finalBalances(requests)) == expected


# T6: two pending requests, accept only one
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/REGISTER/Charlie/70"],
    ["4", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["5", "v1/FRIEND_REQUEST/Alice/Charlie"],
    ["6", "v1/ACCEPT_FRIEND/4"],          # Alice-Bob become friends
    ["7", "v1/SEND_MONEY/Alice/Bob/30"],  # succeeds
    ["8", "v1/SEND_MONEY/Alice/Charlie/30"], # not friends yet -> ignored
]
expected = sorted(["Alice:70", "Bob:80", "Charlie:70"])
assert sorted(finalBalances(requests)) == expected


# ===== END FILE: Robinhood/friendBalanceTracker.py =====

# ===== BEGIN FILE: Robinhood/margincall.py =====

"""
## Customer Portfolio From Trade Stream (with Follow-ups)
You are given a customer’s trade records in timestamp order.
Each trade is a list of strings:

`[timestamp, symbol, side, quantity, price]`

* `side` is `"B"` (buy) or `"S"` (sell)
* `quantity` and `price` are non-negative integers (as strings)
* The customer starts with **cash = 1000** and **0 shares** of every stock.

Return the final portfolio as a list of `[symbol, quantity]` strings:
* Include `["CASH", <cash>]`
* Include only stocks with quantity > 0
* Sort stock symbols alphabetically (CASH can be first)
---

# Follow-up 0 (Base) — Build Portfolio (Tests 1–4)
Process trades in order:

* **Buy**:
  `cash -= quantity * price`
  `shares[symbol] += quantity`

* **Sell**:
  `cash += quantity * price`
  `shares[symbol] -= quantity`
  (Trades are valid: you never sell more than you own.)

Output final portfolio.

---
# Follow-up 2 — Collateral Constraint (Tests 8–10)
Some symbols are **special**: symbols ending with `"O"` (letter O).
For a special stock like `"AAPLO"`, its **collateral stock** is `"AAPL"` (remove the trailing `"O"`).

Constraint (must always hold):
* At all times:
  `shares[collateral] >= shares[special]`

During margin calls:
* You can only sell **non-collateral** shares.
* A collateral stock share is **not sellable** if selling it would break the constraint.
* Special stocks **can be sold**, and selling special shares may free collateral shares to become sellable later.

---

### Notes / Assumptions
* Input is sorted by timestamp.
* All numeric fields are non-negative integers (as strings).
* In base version, trades keep cash non-negative.
* In follow-ups, the margin call rules ensure the process can restore cash to non-negative.

If you want, I can also provide the clean Python solution starting from base → add margin call → add collateral step-by-step.
"""


"""
# Follow-up 1 — Margin Call (Tests 5–7)
Now buys may cause cash to become negative.
After processing a **buy**, if `cash < 0`, perform a **margin call**:

* Force-sell shares from the customer’s portfolio until `cash >= 0`
* You may sell any number of shares of a symbol at its **most recently traded price**
* Sell priority:
  1. Higher most-recent price first
  2. If tie, alphabetically smaller symbol first
* Selling one share adds `price` to cash and decreases shares by 1.
* Margin call may sell shares of the stock that was just bought.
""" 

"""
Follow-up 2 — Collateral Constraint
Special stocks end with "O" (letter O). Example: "AAPLO" is special, collateral is "AAPL".

Constraint must always hold:
shares[collateral] >= shares[special]

During margin call:
You may only sell non-collateral shares
A collateral share is sellable only if it won’t break the constraint
Selling special shares can free collateral shares
"""


import math
from collections import defaultdict

def formatPortfolio(cash, shares):
    result = [['CASH', str(cash)]]
    for symbol in sorted(shares.keys()):
        if shares[symbol] > 0:
            result.append([symbol, str(shares[symbol])])
    return result

def isSpecial(symbol):
    return symbol.endswith('O')

def getSellableShares(symbol, shares, followUp):
    have = shares[symbol]
    if have <= 0:
        return 0
    
    if followUp <= 1: # everything sellable in follow-up 1
        return have
    
    if isSpecial(symbol):
        return have 

    special = symbol + 'O'
    locked = shares[special] # must keep no less than special symbol count

    return max(0, have - locked)

def pickBestSellableSymbol(shares, lastPrice, followUp, soldSpecial):
    bestSymbol = None
    bestPrice = -1

    for symbol in list(shares.keys()):
        if followUp == 2 and symbol in soldSpecial:
            continue
        if getSellableShares(symbol, shares, followUp) <= 0:
            continue

        price = lastPrice[symbol]

        if price > bestPrice or (price == bestPrice and (bestSymbol is None or symbol < bestSymbol)):
            bestPrice = price
            bestSymbol = symbol
    
    return bestSymbol



def runMarginCall(cash, shares, lastPrice, followUp):
    soldSpecial = set()

    while cash < 0:
        bestSymbol = pickBestSellableSymbol(shares, lastPrice, followUp, soldSpecial)
        price = lastPrice[bestSymbol]

        needShares = math.ceil((-cash) / price)
        canSell = getSellableShares(bestSymbol, shares, followUp)
        sellQty = min(needShares, canSell)

        shares[bestSymbol] -= sellQty
        cash += sellQty * price

        if followUp == 2 and isSpecial(bestSymbol):
            soldSpecial.add(bestSymbol)

        if shares[bestSymbol] == 0:
            del shares[bestSymbol]
    
    return cash

def buildPortfolio(trades, followUp):
    # followup 0 base only
    # followup 1 margin call(no collateral)
    # followup 2 margin call + collateral
    cash = 1000
    shares = defaultdict(int)
    lastPrice = {}

    for _,symbol, side, qtyStr, priceStr in trades:
        qty = int(qtyStr)
        price = int(priceStr)
        lastPrice[symbol] = price

        if side == 'B':
            cash -= qty * price
            shares[symbol] += qty

            if followUp >= 1 and cash < 0:
                cash = runMarginCall(cash, shares, lastPrice, followUp)
        else:
            cash += qty * price
            shares[symbol] -= qty
            if shares[symbol] == 0:
                del shares[symbol]
    
    return formatPortfolio(cash, shares)


# =========================
# Test cases for Follow-up 0 / 1 / 2
# Assumes you have:
#   buildPortfolio(trades, followUp)
# where followUp in {0,1,2}
# =========================

# ---------- Follow-up 0 (Base only) ----------
# T0-1: sample 1
trades = [
    ["1", "AAPL", "B", "10", "10"],
    ["3", "GOOG", "B", "20", "5"],
    ["10", "AAPL", "S", "5", "15"],
]
expected = [["CASH", "875"], ["AAPL", "5"], ["GOOG", "20"]]
assert buildPortfolio(trades, 0) == expected

# T0-2: sell all shares -> removed
trades = [
    ["1", "AAPL", "B", "10", "10"],
    ["2", "AAPL", "S", "10", "15"],
]
expected = [["CASH", "1050"]]
assert buildPortfolio(trades, 0) == expected

# T0-3: multiple symbols, alphabetical output
trades = [
    ["1", "MSFT", "B", "1", "100"],
    ["2", "AAPL", "B", "2", "10"],
]
expected = [["CASH", "880"], ["AAPL", "2"], ["MSFT", "1"]]
assert buildPortfolio(trades, 0) == expected


# ---------- Follow-up 1 (Margin call, no collateral) ----------
# T1-1: given margin call example
trades = [
    ["1", "AAPL", "B", "10", "100"],  # cash=0
    ["2", "AAPL", "S", "2", "80"],    # cash=160, AAPL=8, last(AAPL)=80
    ["3", "GOOG", "B", "15", "20"],   # cash=-140 -> margin call sells AAPL(80) 2 shares
]
expected = [["CASH", "20"], ["AAPL", "6"], ["GOOG", "15"]]
assert buildPortfolio(trades, 1) == expected

# T1-2: tie on price => alphabetical symbol first
trades = [
    ["1", "AAPL", "B", "5", "100"],   # cash=500, AAPL=5
    ["2", "ABPL", "B", "5", "100"],   # cash=0, ABPL=5
    ["3", "GOOG", "B", "1", "50"],    # cash=-50 -> sell AAPL first (tie price=100)
]
expected = [["CASH", "50"], ["AAPL", "4"], ["ABPL", "5"], ["GOOG", "1"]]
assert buildPortfolio(trades, 1) == expected

# T1-3: margin call can sell shares of just-bought stock
trades = [
    ["1", "AAPL", "B", "1", "10"],    # cash=990, AAPL=1
    ["2", "GOOG", "B", "100", "20"],  # cash=-1010 -> sell GOOG 51 shares at 20 => cash=10
]
expected = [["CASH", "10"], ["AAPL", "1"], ["GOOG", "49"]]
assert buildPortfolio(trades, 1) == expected


# ---------- Follow-up 2 (Margin call + collateral + no-alternating) ----------
# Uses your provided examples.

# T2-1: Example 1
trades = [
    ["1", "AAPL",  "B", "5", "100"],
    ["2", "GOOG",  "B", "5", "60"],
    ["3", "GOOGO", "B", "5", "40"],  # special, collateral=GOOG
    ["5", "AAPLO", "B", "5", "30"],  # special, collateral=AAPL
]
expected = [["CASH", "10"], ["AAPL", "5"], ["AAPLO", "5"], ["GOOG", "5"], ["GOOGO", "1"]]
assert buildPortfolio(trades, 2) == expected

# T2-2: Example 2
trades = [
    ["1", "AAPL",  "B", "8",  "100"],
    ["2", "AAPLO", "B", "5",  "40"],
    ["3", "GOOG",  "B", "20", "30"],
]
expected = [["CASH", "0"], ["AAPL", "4"], ["GOOG", "20"]]
assert buildPortfolio(trades, 2) == expected

# T2-3: Example 3
trades = [
    ["1", "AAPL",  "B", "6",  "100"],
    ["2", "GOOG",  "B", "5",  "60"],
    ["3", "GOOGO", "B", "5",  "40"],
    ["5", "AAPLO", "B", "5",  "30"],
]
expected = [["CASH", "10"], ["AAPL", "5"], ["AAPLO", "5"], ["GOOG", "5"], ["GOOGO", "1"]]
assert buildPortfolio(trades, 2) == expected


print("All tests passed!")



# ===== END FILE: Robinhood/margincall.py =====

# ===== BEGIN FILE: Robinhood/maximumMultiplierPath.py =====

"""
Maximum Multiplier Path
You are given a directed graph with n nodes labeled 0 .. n-1.
Each directed edge is [u, v, w], meaning you can go from u to v and multiply your current value by w.
You are also given two nodes: start and end.

Task
Find the maximum product of multipliers along any simple path from start to end.
A simple path means you cannot visit the same node more than once.
If no simple path exists from start to end, return -1.

Input
n: int
edges: List[List[int]] where each edge is [u, v, w]
start: int
end: int

Output
int: the maximum product, or -1 if impossible

Constraints
1 <= w <= 1e5
0 <= start, end < n
The graph may contain cycles, but your chosen path must be simple.
"""
# from collections import defaultdict
# import heapq

from typing import List, Tuple

def maxMultiplierProduct(self, n: int, edges: List[List[int]], start: int, end: int) -> int:
    g = [[] for _ in range(n)]

    for u, v, w in edges:
        g[u].append((v, w))
    
    # simple path rule: no node can be visited twice
    visited = set()

    def dfs(u):
        if u == end:
            return 1
        visited.add(u)
        best = -1

        for v, w in g[u]:
            if v in visited:
                continue
            sub = dfs(v)
            if sub != -1: # has a valid path
                best = max(best, w * sub)
        
        visited.remove(u) # restore the path
        return best
    
    return dfs(start)



# T1: Example 1 (best path is 0->1->2->4->3)
n = 5
edges = [[0, 1, 2], [1, 2, 3], [2, 1, 4], [1, 3, 5], [2, 4, 6], [4, 3, 10]]
start, end = 0, 3
expected = 360
assert maxMultiplierProduct(n, edges, start, end) == expected


# T2: Example 2 (cycle exists, but best simple path is 0->1->3)
n = 4
edges = [[0, 1, 1], [1, 2, 2], [2, 1, 3], [1, 3, 4]]
start, end = 0, 3
expected = 4
assert maxMultiplierProduct(n, edges, start, end) == expected


# T3: Example 3 (end is unreachable from start)
n = 6
edges = [[0, 1, 2], [1, 2, 3], [2, 0, 4], [3, 4, 5], [4, 5, 6]]
start, end = 0, 3
expected = -1
assert maxMultiplierProduct(n, edges, start, end) == expected


# T4: Start equals end (empty path is allowed -> product = 1)
n = 3
edges = [[0, 1, 5], [1, 2, 7]]
start, end = 1, 1
expected = 1
assert maxMultiplierProduct(n, edges, start, end) == expected


# T5: Multiple paths exist, choose the maximum product
# 0->1->3 = 2*3=6
# 0->2->3 = 10*1=10 (best)
n = 4
edges = [[0, 1, 2], [1, 3, 3], [0, 2, 10], [2, 3, 1]]
start, end = 0, 3
expected = 10
assert maxMultiplierProduct(n, edges, start, end) == expected


# T6: Critical case: a "gain cycle" (product > 1) exists.
# The problem requires a SIMPLE path (no repeated nodes), so the answer is finite.
# Best simple path: 0->1->2->3 = 2*2*2 = 8
# If cycles were allowed, the product could grow without bound.
n = 4
edges = [[0, 1, 2], [1, 2, 2], [2, 1, 2], [2, 3, 2]]
start, end = 0, 3
expected = 8
assert maxMultiplierProduct(n, edges, start, end) == expected


# ===== END FILE: Robinhood/maximumMultiplierPath.py =====

# ===== BEGIN FILE: Robinhood/offsetCommit.py =====

"""
## Offset Commit Ordering
You process messages from a stream.
Each message has a unique integer **offset** starting from **0**.

Messages may be **processed out of order** (multi-threaded), but a **commit** must always be **contiguous from 0**:
* Committing offset `x` means offsets `0..x` are all done.
* After processing each offset, if you have a continuous completed block `0..k`, you must commit **the largest such `k`**.
* If offset `0` is not yet processed (or the block is broken), you cannot commit anything and output `-1`.

### Task
Given an array `offsets` in the order they are processed, return an array `res` of the same length:
* `res[i] = k` if after processing `offsets[i]` you can commit up to `k` (the largest contiguous block from 0)
* otherwise `res[i] = -1`

### Example
Input: `offsets = [2, 0, 1]`
Output: `[-1, 0, 2]`
"""

def commitOffsets(offsets):
    seen = set()
    nextCommit = 0
    res = []

    for x in offsets:
        seen.add(x)

        before = nextCommit
        while nextCommit in seen:
            nextCommit += 1
        
        if nextCommit > before:
            res.append(nextCommit - 1)
        else:
            res.append(-1)
    return res

# T1: example 1
offsets = [2, 0, 1]
expected = [-1, 0, 2]
assert commitOffsets(offsets) == expected

# T2: example 2
offsets = [0, 1, 2]
expected = [0, 1, 2]
assert commitOffsets(offsets) == expected

# T3: example 3
offsets = [2, 1, 0, 5, 4]
expected = [-1, -1, 2, -1, -1]
assert commitOffsets(offsets) == expected

# T4: single offset 0
offsets = [0]
expected = [0]
assert commitOffsets(offsets) == expected

# T5: start missing for a while
offsets = [3, 2, 1, 0]
expected = [-1, -1, -1, 3]
assert commitOffsets(offsets) == expected

# T6: gaps remain unfilled
offsets = [0, 2, 4, 1]
expected = [0, -1, -1, 2]
assert commitOffsets(offsets) == expected

# T7: larger jump after filling gaps
offsets = [5, 0, 1, 4, 2, 3]
expected = [-1, 0, 1, -1, 2, 5]
assert commitOffsets(offsets) == expected


# ===== END FILE: Robinhood/offsetCommit.py =====

# ===== BEGIN FILE: Robinhood/portfolioValueOptimization.py =====

"""
Portfolio Value Optimization
You have some securities available to buy that each has a price Pi.
Your friend predicts for each security the stock price will be Si at some future date.
But based on volatility of each share, you only want to buy up to Ai shares of each security i.
Given M dollars to spend, calculate the maximum value you could potentially
achieve based on the predicted prices Si (and including any cash you have remaining).

Pi = Current Price
Si = Expected Future Price
Ai = Maximum units you are willing to purchase
M = Dollars available to invest
Example 1:
Input:
M = $140 available
N = 4 Securities
P1=15, S1=45, A1=3 (AAPL)
P2=40, S2=50, A2=3 (BYND)
P3=25, S3=35, A3=3 (SNAP)
P4=30, S4=25, A4=4 (TSLA)

Output: $265 (no cash remaining) 
3 shares of apple -> 45(15 *3), 135(45 *3)
3 shares of snap -> 75, 105
0.5 share of bynd -> 20, 25
"""
def maxPortfolioValue(M, sec):
    deals = []
    for symbol, p, s, a in sec:
        p = float(p)
        s = float(s)
        a = float(a)
        if s > p:
            deals.append((s / p, p, s, a))
    
    deals.sort(reverse = True, key = lambda x: x[0])

    cash = float(M)
    future = cash

    for _, p, s, a in deals:
        if cash <= 0:
            break

        spend = min(cash, p * a)
        shares = spend / p 

        cash -= spend
        future += shares * (s - p)

    return future # time: O(nlgn) space: O(n)


# T1: sample 1 (mix full + fractional buy, skip losing stock)
M = 140
sec = [
    ["AAPL", "15", "45", "3"],
    ["BYND", "40", "50", "3"],
    ["SNAP", "25", "35", "3"],
    ["TSLA", "30", "25", "4"],
]
# buy 3 AAPL (cost 45, future 135), 3 SNAP (cost 75, future 105), 0.5 BYND (cost 20, future 25)
expected = 265.0
assert maxPortfolioValue(M, sec) == expected


# T2: sample 2 (no profitable trades -> keep all cash)
M = 100
sec = [
    ["AAPL", "15", "10", "3"],
    ["BYND", "40", "35", "3"],
]
expected = 100.0
assert maxPortfolioValue(M, sec) == expected


# T3: sample 3 (best ROI first, then remainder cash)
M = 50
sec = [
    ["SNAP", "20", "30", "5"],  # ROI=1.5
    ["AAPL", "50", "70", "2"],  # ROI=1.4
]
# buy 2.5 SNAP (spend 50) -> future 2.5*30 = 75
expected = 75.0
assert maxPortfolioValue(M, sec) == expected


# T4: fractional across a cap (can't exceed Ai)
M = 100
sec = [
    ["X", "10", "20", "3"],   # can spend at most 30
    ["Y", "10", "15", "100"], # spend rest here
]
# buy 3 X -> spend 30, future 60
# remaining 70 -> buy 7 Y -> future 105
expected = 165.0
assert maxPortfolioValue(M, sec) == expected


# T5: exact budget not required (leftover cash kept)
M = 7
sec = [
    ["A", "5", "6", "1"],  # spend at most 5, profit small
]
# buy 1 share: spend 5, future value = 6 + leftover cash 2 = 8
expected = 8.0
assert maxPortfolioValue(M, sec) == expected


# T6: tie ROI (either order yields same future value)
M = 10
sec = [
    ["A", "2", "4", "2"],  # ROI=2, max spend 4
    ["B", "3", "6", "2"],  # ROI=2, max spend 6
]
# spend all 10 at ROI 2 => future 20
expected = 20.0
assert maxPortfolioValue(M, sec) == expected


# ===== END FILE: Robinhood/portfolioValueOptimization.py =====

# ===== BEGIN FILE: Robinhood/stockTradesMatching(follow-up-todo).py =====

"""
## Stock Trades Matching (Robinhood)

A trade is a fixed-width string with 4 comma-separated fields:

`"<SYMBOL>,<SIDE>,<QTY>,<ID>"`

* `SYMBOL`: 4 characters, uppercase letters, **left-padded with spaces** (e.g. `"  FB"`, `"AAPL"`)
* `SIDE`: `"B"` (buy) or `"S"` (sell)
* `QTY`: 4 digits, **left-padded with zeros** (e.g. `"0010"`)
* `ID`: 6 alphanumeric characters

Example:
`"AAPL,B,0100,ABC123"`
---
### Input
* `house_trades: List[str]`
* `street_trades: List[str]`
Trades are **distinct but not unique** (duplicates may exist).
---

### Matching Rules (apply in this priority order)

1. **Exact Match (highest priority)**
   Match one house trade with one street trade if **all 4 fields are identical**:
   `SYMBOL, SIDE, QTY, ID`

2. **Fuzzy Match (follow-up 1)**
   After all exact matches are removed, match one house trade with one street trade if:

* `SYMBOL, SIDE, QTY` are identical
* `ID` is ignored

Tie-break (when multiple possible matches):

* match the **alphabetically earliest** remaining house trade with the **alphabetically earliest** remaining street trade

3. **Offsetting Match (follow-up 2)**
   After exact + fuzzy matches are removed, match trades **within the same list** (house with house, or street with street) if:

* `SYMBOL` and `QTY` are identical
* `SIDE` is opposite (`B` vs `S`)

Tie-break:

* match the **alphabetically earliest buy** with the **alphabetically earliest sell**

---

### Output

Return all **unmatched** trades from both lists as:

* `List[str]` sorted in **ascending lexicographical order** (string order)

---

### Examples

#### TEST1 (Exact match)

```text
house_trades  = ["AAPL,B,0100,ABC123", "GOOG,S,0050,CDC333"]
street_trades = ["  FB,B,0100,GBGGGG", "AAPL,B,0100,ABC123"]

output = ["  FB,B,0100,GBGGGG", "GOOG,S,0050,CDC333"]
```

#### TEST2 (Duplicates + exact match)

```text
house_trades  = ["AAPL,S,0010,ZYX444",
                 "AAPL,S,0010,ZYX444",
                 "AAPL,B,0010,ABC123",
                 "GOOG,S,0050,GHG545"]
street_trades = ["GOOG,S,0050,GHG545",
                 "AAPL,S,0010,ZYX444",
                 "AAPL,B,0010,TTT222"]

output = ["AAPL,S,0010,ZYX444"]
```

#### TEST3 (Multiple duplicates)

```text
house_trades  = ["AAPL,B,0100,ABC123",
                 "AAPL,B,0100,ABC123",
                 "AAPL,B,0100,ABC123",
                 "GOOG,S,0050,CDC333"]
street_trades = ["  FB,B,0100,GBGGGG",
                 "AAPL,B,0100,ABC123"]

output = ["  FB,B,0100,GBGGGG",
          "AAPL,B,0100,ABC123",
          "AAPL,B,0100,ABC123",
          "GOOG,S,0050,CDC333"]
```
"""
from collections import Counter, defaultdict
from typing import List, Tuple, Dict

def getUnmatchedTrades(houseTrades, streetTrades):
    house = Counter(houseTrades)
    street = Counter(streetTrades)

    cache = {}

    def parse(t):
        if t not in cache:
            cache[t] = tuple(t.split(','))
        return cache[t]
    
    def dec(cnt, key, k):
        if k <= 0:
            return
        newv = cnt[key] - k 
        if newv <= 0:
            cnt.pop(key, None) # del cnt[key]
        else:
            cnt[key] = newv

    # exact match    
    for t in list(house.keys() & street.keys()):
        m = min(house[t], street[t])
        dec(house, t, m)
        dec(street, t, m)
    

    # fuzzy matches
    def groupByFuzzy(cnt):
        groups = defaultdict(list)
        for t, c in cnt.items():
            sym, side, qty, _ = parse(t)
            groups[(sym, side, qty)].append([t, c])
        for k in groups:
            # sort list in same key with lexico order of order strs
            groups[k].sort(key = lambda x: x[0])
        return groups
    
    houseF = groupByFuzzy(house)
    streetF = groupByFuzzy(street)

    for k in (houseF.keys() & streetF.keys()):
        hlist = houseF[k]
        slist = streetF[k]
        i = j = 0
        while i < len(hlist) and j < len(slist):
            ht, hc = hlist[i]
            st, sc = slist[j]
            m = min(hc, sc)

            dec(house, ht, m)
            dec(street, st, m)

            hc -= m
            sc -= m 
            hlist[i][1] = hc
            slist[j][1] = sc 

            if hc == 0:
                i += 1
            if sc == 0:
                j += 1
    
    # offsetting matches
    def offsetWithOneSide(cnt):
        buys = defaultdict(list) # (sym, qty) -> [[tradeStr, count], ... ]
        sells = defaultdict(list)

        for t, c in cnt.items():
            sym, side, qty, _ = parse(t)
            key = (sym, qty)

            (buys if side == 'B' else sells)[key].append([t, c])

        
        for k in buys:
            buys[k].sort(key = lambda x: x[0])
        
        for k in sells:
            sells[k].sort(key = lambda x: x[0])
        
        for key in (buys.keys() & sells.keys()):
            blist = buys[key]
            slist = sells[key]
            i = j = 0
            while i < len(blist) and j < len(slist):
                bt, bc = blist[i]
                st, sc = slist[j]
                m = min(bc, sc)

                dec(cnt, bt, m)
                dec(cnt, st, m)
                bc -= m
                sc -= m 
                blist[i][1] = bc 
                slist[j][1] = sc

                if bc == 0:
                    i += 1
                if sc == 0:
                    j += 1

    offsetWithOneSide(house)
    offsetWithOneSide(street)


    res = []
    for t, c in house.items():
        res.extend([t] * c)
    
    for t, c in street.items():
        res.extend([t] * c)
    
    res.sort()
    return res



testCases = [
    # Tests 1-5: Exact
    {
        "name": "TEST1_exact_basic",
        "house_trades": ["AAPL,B,0100,ABC123", "GOOG,S,0050,CDC333"],
        "street_trades": ["  FB,B,0100,GBGGGG", "AAPL,B,0100,ABC123"],
        "expected": ["  FB,B,0100,GBGGGG", "GOOG,S,0050,CDC333"],
    },
    {
        "name": "TEST2_exact_duplicates",
        "house_trades": [
            "AAPL,S,0010,ZYX444",
            "AAPL,S,0010,ZYX444",
            "AAPL,B,0010,ABC123",
            "GOOG,S,0050,GHG545",
        ],
        "street_trades": [
            "GOOG,S,0050,GHG545",
            "AAPL,S,0010,ZYX444",
            "AAPL,B,0010,TTT222",
        ],
        "expected": ["AAPL,S,0010,ZYX444"],
    },
    {
        "name": "TEST3_exact_more_duplicates",
        "house_trades": [
            "AAPL,B,0100,ABC123",
            "AAPL,B,0100,ABC123",
            "AAPL,B,0100,ABC123",
            "GOOG,S,0050,CDC333",
        ],
        "street_trades": ["  FB,B,0100,GBGGGG", "AAPL,B,0100,ABC123"],
        "expected": [
            "  FB,B,0100,GBGGGG",
            "AAPL,B,0100,ABC123",
            "AAPL,B,0100,ABC123",
            "GOOG,S,0050,CDC333",
        ],
    },
    {
        "name": "TEST4_exact_no_match_all_returned_sorted",
        "house_trades": ["AAPL,B,0100,AAA111", "GOOG,S,0050,BBB222"],
        "street_trades": ["MSFT,B,0001,CCC333"],
        "expected": ["AAPL,B,0100,AAA111", "GOOG,S,0050,BBB222", "MSFT,B,0001,CCC333"],
    },
    {
        "name": "TEST5_exact_multiple_exact_pairs_leftover",
        "house_trades": ["AAPL,B,0100,AAA111", "AAPL,B,0100,AAA111", "AAPL,S,0100,AAA111"],
        "street_trades": ["AAPL,B,0100,AAA111", "AAPL,S,0100,AAA111"],
        "expected": ["AAPL,B,0100,AAA111"],
    },

    # Tests 6-9: Fuzzy
    {
        "name": "TEST6_fuzzy_simple_id_diff",
        "house_trades": ["AAPL,B,0100,AAA111"],
        "street_trades": ["AAPL,B,0100,BBB222"],
        "expected": [],
    },
    {
        "name": "TEST7_fuzzy_exact_has_priority",
        "house_trades": ["AAPL,B,0100,AAA111", "AAPL,B,0100,BBB222"],
        "street_trades": ["AAPL,B,0100,AAA111"],
        "expected": ["AAPL,B,0100,BBB222"],
    },
    {
        "name": "TEST8_fuzzy_tie_break_earliest_alpha",
        "house_trades": ["AAPL,B,0100,BBB222", "AAPL,B,0100,AAA111"],
        "street_trades": ["AAPL,B,0100,DDD444", "AAPL,B,0100,CCC333"],
        "expected": [],
    },
    {
        "name": "TEST9_fuzzy_with_counts_earliest_consumed_first",
        "house_trades": ["AAPL,B,0100,AAA111", "AAPL,B,0100,AAA111", "AAPL,B,0100,BBB222"],
        "street_trades": ["AAPL,B,0100,BBB999", "AAPL,B,0100,BBB999"],
        "expected": ["AAPL,B,0100,BBB222"],
    },

    # Test 10: Offsetting
    {
        "name": "TEST10_offsetting_within_house",
        "house_trades": ["AAPL,B,0100,AAA111", "AAPL,S,0100,ZZZ999", "AAPL,S,0100,BBB222"],
        "street_trades": [],
        "expected": ["AAPL,S,0100,ZZZ999"],
    },
]


def runTests():
    for t in testCases:
        got = getUnmatchedTrades(t["house_trades"], t["street_trades"])
        assert got == t["expected"], f'{t["name"]} FAILED\n got={got}\n exp={t["expected"]}'
    print("All tests passed!")


runTests()

# ===== END FILE: Robinhood/stockTradesMatching(follow-up-todo).py =====

# ===== BEGIN FILE: Robinhood/test.py =====

from collections import defaultdict

def finalBalances(requests):
    balance = {}
    friends = defaultdict(set) # undirected
    pending = {} # seqId -> (fromUser, toUser)

    for seqId, path in requests:
        parts = path.split('/')
        action = parts[1]

        if action == 'REGISTER':
            user = parts[2]
            balance[user] = int(parts[3])
        elif action == 'FRIEND_REQUEST':
            fromUser, toUser = parts[2], parts[3]
            pending[seqId] = (fromUser, toUser)
        elif action == 'ACCEPT_FRIEND':
            reqId = parts[2]
            if reqId in pending:
                a, b = pending.pop(reqId)
                friends[a].add(b)
                friends[b].add(a)
        else:
            f, t, c = parts[2], parts[3], int(parts[-1])

            if t in friends[f] and balance[f] >= c:
                balance[f] -= c
                balance[t] += c

    return [f'{user}:{bal}' for user, bal in balance.items()]


# T1: sample 1 (friendship required)
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/REGISTER/Charlie/75"],
    ["4", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["5", "v1/ACCEPT_FRIEND/4"],
    ["6", "v1/SEND_MONEY/Alice/Bob/30"],
    ["7", "v1/SEND_MONEY/Charlie/Alice/25"],  # not friends -> ignored
]
expected = sorted(["Alice:70", "Bob:80", "Charlie:75"])
assert sorted(finalBalances(requests)) == expected


# T2: sample 2 (two-way transfers after being friends)
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/REGISTER/Charlie/75"],
    ["4", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["5", "v1/ACCEPT_FRIEND/4"],
    ["6", "v1/SEND_MONEY/Alice/Bob/20"],
    ["7", "v1/SEND_MONEY/Bob/Alice/10"],
]
expected = sorted(["Alice:90", "Bob:60", "Charlie:75"])
assert sorted(finalBalances(requests)) == expected


# T3: sample 3 (send money without friendship -> ignored)
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/SEND_MONEY/Alice/Bob/30"],  # not friends -> ignored
]
expected = sorted(["Alice:100", "Bob:50"])
assert sorted(finalBalances(requests)) == expected


# T4: insufficient balance -> ignored
requests = [
    ["1", "v1/REGISTER/Alice/10"],
    ["2", "v1/REGISTER/Bob/0"],
    ["3", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["4", "v1/ACCEPT_FRIEND/3"],
    ["5", "v1/SEND_MONEY/Alice/Bob/20"],  # Alice has only 10 -> ignored
]
expected = sorted(["Alice:10", "Bob:0"])
assert sorted(finalBalances(requests)) == expected


# T5: accept unknown friend request id -> ignored
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/100"],
    ["3", "v1/ACCEPT_FRIEND/999"],        # no such pending request
    ["4", "v1/SEND_MONEY/Alice/Bob/10"],  # still not friends -> ignored
]
expected = sorted(["Alice:100", "Bob:100"])
assert sorted(finalBalances(requests)) == expected


# T6: two pending requests, accept only one
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/REGISTER/Charlie/70"],
    ["4", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["5", "v1/FRIEND_REQUEST/Alice/Charlie"],
    ["6", "v1/ACCEPT_FRIEND/4"],          # Alice-Bob become friends
    ["7", "v1/SEND_MONEY/Alice/Bob/30"],  # succeeds
    ["8", "v1/SEND_MONEY/Alice/Charlie/30"], # not friends yet -> ignored
]
expected = sorted(["Alice:70", "Bob:80", "Charlie:70"])
assert sorted(finalBalances(requests)) == expected


# ===== END FILE: Robinhood/test.py =====

# ===== BEGIN FILE: Robinhood/triggerCount.py =====

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

# ===== END FILE: Robinhood/triggerCount.py =====

# ===== BEGIN FILE: Uber/CPUUsageAnalysis.py =====

"""
Given a list of log events represented as a 2D string array logs, where each log entry contains three elements: task_name, 
an action ("enter" or "exit"), and a timestamp:
"enter" indicates the start of a task.
"exit" indicates the completion of a task.
Calculate the total time the CPU spends executing each task. 
Return the results as a list of strings in the format "task_name: total_time", sorted alphabetically by task names.

Note that the CPU is single-threaded, meaning it can only process one task at a time. Tasks may overlap, and when the CPU completes a task, if multiple tasks are waiting, it always resumes the most recently added task.
"""
from collections import defaultdict
class Solution:
    def cpuTimeByTask(self, logs):
        logs.sort(key = lambda x: int(x[2])) # sort by timestamp first

        timeByTask = defaultdict(int) # total cpu time spent running this task
        stack = [] # call stack of currently active tasks

        # prevTime is timestamp of the last processed log event
        # the time interval (prevTime -> currentTime) belongs to stack[-1]
        prevTime = None 

        for task, action, tsStr in logs:
            ts = int(tsStr)

            if prevTime is None:
                prevTime = ts
            
            # time since prevTime belongs to current running task 
            if stack:
                timeByTask[stack[-1]] += ts - prevTime

            # now handle the current event at time ts:
            if action == 'enter':
                stack.append(task)
            else:
                stack.pop()
            
            # more prevTime forward to current timestamp for the next interval
            prevTime = ts
        
        return [f'{name}: {timeByTask[name]}' for name in sorted(timeByTask)]


def runTests():
    sol = Solution()

    logs1 = [
        ["print", "enter", "10"],
        ["malloc", "enter", "12"],
        ["malloc", "exit", "14"],
        ["write", "enter", "16"],
        ["write", "exit", "18"],
        ["write", "enter", "20"],
        ["write", "exit", "22"],
        ["print", "exit", "24"],
    ]
    assert sol.cpuTimeByTask(logs1) == ["malloc: 2", "print: 8", "write: 4"]

    logs2 = [
        ["task1", "enter", "0"],
        ["task3", "exit", "6"],
        ["task2", "exit", "8"],
        ["task2", "enter", "2"],
        ["task3", "enter", "4"],
        ["task1", "exit", "10"],
    ]
    assert sol.cpuTimeByTask(logs2) == ["task1: 4", "task2: 4", "task3: 2"]

    logs3 = [
        ["taskA", "enter", "0"],
        ["taskA", "exit", "5"],
        ["taskA", "enter", "6"],
        ["taskA", "exit", "10"],
        ["taskB", "enter", "10"],
        ["taskB", "exit", "15"],
    ]
    assert sol.cpuTimeByTask(logs3) == ["taskA: 9", "taskB: 5"]

    print("All tests passed!")


runTests()


# ===== END FILE: Uber/CPUUsageAnalysis.py =====

# ===== BEGIN FILE: Uber/FindRobotsPosition.py =====

"""
You are given a m * n board representing a position map and an array representing distances to the nearest blocker from a robot's position. The board is a 2D array where each cell can be:

'O': Represents a robot.
'E': Represents an empty space.
'X': Represents a blocker.
The boundary of the board is also considered a blocker. Additionally, you are provided with a distance array of four integers, which correspond to the distances to the closest blocker in the following order: left, top, bottom, and right.

Write a function that takes the position map and the distance array as inputs and returns the indices of all robots that match the given distance criteria.

Constraints:

The board dimensions are at least 1x1.
The distance array contains exactly four integers.
The matrix only contains 'O', 'E' and 'X'
"""
def findMatchingRobots(board, distance):
    m, n = len(board), len(board[0])
    targetLeft, targetTop, targetBottom, targetRight = distance

    leftDist = [[0] * n for _ in range(m)]
    rightDist = [[0] * n for _ in range(m)]
    topDist = [[0] * n for _ in range(m)]
    bottomDist = [[0] * n for _ in range(m)]


    for r in range(m):
        lastBlocker = -1
        for c in range(n):
            if board[r][c] == 'X':
                lastBlocker = c
            else:
                leftDist[r][c] = c - lastBlocker

        nextBlocker = n 
        for c in range(n - 1, -1, -1):
            if board[r][c] == 'X':
                nextBlocker = c
            else:
                rightDist[r][c] = nextBlocker - c
        
    for c in range(n):
        lastBlocker = -1
        for r in range(m):
            if board[r][c] == 'X':
                lastBlocker = r
            else:
                topDist[r][c] = r - lastBlocker
        
        nextBlocker = m
        for r in range(m - 1, -1, -1):
            if board[r][c] == 'X':
                nextBlocker = r
            else:
                bottomDist[r][c] = nextBlocker - r
    
    res = []
    for r in range(m):
        for c in range(n):
            if board[r][c] != 'O':
                continue
            if (leftDist[r][c] == targetLeft and
                topDist[r][c] == targetTop and
                bottomDist[r][c] == targetBottom and
                rightDist[r][c] == targetRight):
                res.append([r, c])
    
    return res

# Quick tests (from examples)
board1 = [
    ["O","E","E","E","X"],
    ["E","O","X","X","X"],
    ["E","E","E","E","E"],
    ["X","E","O","E","E"],
    ["X","E","X","E","X"]
]
assert findMatchingRobots(board1, [2,2,4,1]) == [[1,1]]

board2 = [
    ["O","E","X","O","O"],
    ["E","O","X","O","X"],
    ["X","X","O","E","E"],
    ["E","O","E","O","E"],
    ["O","O","X","O","O"]
]
assert findMatchingRobots(board2, [2,1,2,4]) == [[3,1]]

board3 = [
    ["O","X","O"],
    ["E","O","X"],
    ["O","X","O"]
]
# order depends on scan (row-major)
assert findMatchingRobots(board3, [1,1,1,1]) == [[0,2],[2,2]] or findMatchingRobots(board3, [1,1,1,1]) == [[2,2],[0,2]]


# ===== END FILE: Uber/FindRobotsPosition.py =====

# ===== BEGIN FILE: Uber/MeetingScheduler.py =====

"""
Design a meeting room scheduler for a predefined set of meeting rooms identified by their unique room IDs (e.g., ["roomA", "roomB", ...]).
Implement the MeetingScheduler class:

MeetingScheduler(List<String> roomList) Initializes the scheduler system with the given list of room IDs.
String schedule(int start, int end) Schedule a meeting in one of the available rooms between the start and end time.

If multiple rooms are available, assign the room with the lexicographically smallest room ID.
If no rooms are available for the specified time slot, return an empty string.
"""
from bisect import bisect_left
class MeetingScheduler:
    def __init__(self, roomList):
        self.rooms = sorted(roomList)
        self.roomMeetings = { roomId: [] for roomId in self.rooms }
    
    def schedule(self, start, end):
        for roomId in self.rooms:
            meetings = self.roomMeetings[roomId]

            idx = bisect_left(meetings, (start, end))

            if idx > 0 and meetings[idx - 1][1] > start:
                continue

            if idx < len(meetings) and meetings[idx][0] < end:
                continue
                
            meetings.insert(idx, (start, end))
            return roomId
        return ''
    
def runTests():
    # Example 1
    scheduler = MeetingScheduler(["roomB", "roomA", "roomC"])
    assert scheduler.schedule(1, 5) == "roomA"
    assert scheduler.schedule(1, 5) == "roomB"
    assert scheduler.schedule(2, 6) == "roomC"
    assert scheduler.schedule(2, 3) == ""
    assert scheduler.schedule(5, 10) == "roomA"
    assert scheduler.schedule(8, 10) == "roomB"

    # Example 2
    scheduler = MeetingScheduler(["roomA"])
    assert scheduler.schedule(1, 5) == "roomA"
    assert scheduler.schedule(1, 5) == ""
    assert scheduler.schedule(5, 10) == "roomA"
    assert scheduler.schedule(2, 6) == ""

    # Example 3
    scheduler = MeetingScheduler(["roomA", "roomB"])
    assert scheduler.schedule(1, 3) == "roomA"
    assert scheduler.schedule(2, 4) == "roomB"
    assert scheduler.schedule(3, 5) == "roomA"
    assert scheduler.schedule(1, 2) == "roomB"   # fits before [2,4)
    assert scheduler.schedule(4, 6) == "roomB"   # fits after [2,4)
    assert scheduler.schedule(8, 10) == "roomA"

    print("All tests passed!")


runTests()


# ===== END FILE: Uber/MeetingScheduler.py =====

# ===== BEGIN FILE: Uber/MinimizConvexFunction.py =====

"""
You are given access to a black-box function, F(x), which is convex over a given closed interval [a, b]. 
You can only interact with this function by calling a provided evaluate(x) function, which returns the value of F(x).
Your task is to find a point x* within the interval [a, b] that is within a specified precision, eps, 
of the true location of the minimum. In other words, if x_min is the point where the function's minimum occurs, 
find an x* such that |x* - x_min| ≤ eps.
Hint: A key property of a convex function on an interval is that it is unimodal, meaning it has a single minimum. 
This property allows for efficient search algorithms.
"""
import math
class ConvexFunction:
    def __init__(self, func):
        self.func = func
    
    def evaluate(self, x):
        return self.func(x)
    
class Solution:
    def __init__(self, func):
        self.func = func
    
    def minimize(self, a, b, eps):
        while (b - a) > eps:
            m1 = a + (b - a) / 3
            m2 = b - (b - a) / 3

            f1 = self.func.evaluate(m1)
            f2 = self.func.evaluate(m2)

            if f1 < f2:
                b = m2
            else:
                a = m1
        return (a + b) / 2

def test1():
    print("===== Test 1 =====")
    func = ConvexFunction(lambda x: (x - 3)**2 + 5)
    solution = Solution(func)
    result = solution.minimize(-10, 10, 0.01)
    print(f"Result: {result}")  # Expected: ~3.0

def test2():
    print("===== Test 2 =====")
    func = ConvexFunction(lambda x: x**2)
    solution = Solution(func)
    result = solution.minimize(-100, 50, 0.001)
    print(f"Result: {result}")  # Expected: ~0.0

def test3():
    print("===== Test 3 =====")
    func = ConvexFunction(lambda x: abs(x - 123.456))
    solution = Solution(func)
    result = solution.minimize(0, 1000, 0.0001)
    print(f"Result: {result}")  # Expected: ~123.456

def test4():
    print("===== Test 4 =====")
    func = ConvexFunction(lambda x: (x - 987.654)**2)
    solution = Solution(func)
    result = solution.minimize(-1e9, 1e9, 1e-4)
    print(f"Result: {result}")  # Expected: ~987.654

def test5():
    print("===== Test 5 =====")
    func = ConvexFunction(lambda x: math.exp(x) - 2 * x)
    solution = Solution(func)
    result = solution.minimize(0, 2, 1e-4)
    print(f"Result: {result}")  # Expected: ~0.693

def test6():
    print("===== Test 6 =====")
    func = ConvexFunction(lambda x: x)
    solution = Solution(func)
    result = solution.minimize(0, 100, 1e-4)
    print(f"Result: {result}")  # Expected: ~0.0

def test7():
    print("===== Test 7 =====")
    func = ConvexFunction(lambda x: (x - 1)**2)
    solution = Solution(func)
    result = solution.minimize(0.9999, 1.0001, 1e-4)
    print(f"Result: {result}")  # Expected: ~1.0

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()

# ===== END FILE: Uber/MinimizConvexFunction.py =====

# ===== BEGIN FILE: Uber/MinimumCostBuyAllWordswithPrefixBundles.py =====

"""
Question: Minimum Cost to Buy All Words with Prefix Bundles
You are given a list of distinct words. You want to “buy” all of them with minimum total cost.
You have two types of purchases:
Buy a single word
You can buy a specific word w for cost wordCost[w].
Buy a prefix bundle
You can buy a bundle for a prefix p for cost bundleCost[p].
Buying prefix p purchases all words that start with p.
You may buy any combination of single words and prefix bundles.
A word is considered purchased if it is covered by at least one purchase (either directly or by a prefix bundle).

Goal
Return the minimum total cost to purchase all words.

Input
words: List[str] — list of words to purchase
wordCost: Dict[str, int] — cost to buy each word individually
bundleCost: Dict[str, int] — cost to buy each prefix bundle (prefix can be any length)

Output
minTotalCost: int

Notes / Assumptions
All costs are non-negative integers.
Every word in words exists as a key in wordCost.
bundleCost may contain prefixes that match no word; those bundles are useless and can be ignored.

Output only the minimum total cost (no need to output which purchases were made).
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.wordCost = None
        self.bundleCost = None
    
def minCostBuyAllWords(words, wordCost, bundleCost):
    root = TrieNode()

    # Insert all words
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        # reach the end letter of word, add wordCost
        node.wordCost = wordCost[w]

    # Insert all bundle prefixes (even if no word currently matches)
    for prefix, cost in bundleCost.items():
        node = root
        for ch in prefix:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.bundleCost = cost if node.bundleCost is None else min(node.bundleCost, cost)

    def dfs(node):
        # if node is complete word node, update baseCost
        baseCost = (node.wordCost or 0)
        # sum all children's cost
        for child in node.children.values():
            baseCost += dfs(child)

        if node.bundleCost is None:
            return baseCost
        # compare prefix cost and all individual child cost
        return min(baseCost, node.bundleCost)

    return dfs(root)
    
# ---------- Test cases ----------
def runTests() -> None:
    # 1) No bundles -> must buy all singles
    words = ["photo", "phoeo", "phose", "phcertd"]
    wordCost = {"photo": 5, "phoeo": 6, "phose": 4, "phcertd": 20}
    bundleCost = {}
    assert minCostBuyAllWords(words, wordCost, bundleCost) == 35

    # 2) Simple prefix bundles (like your 3-letter example)
    bundleCost2 = {"pho": 12, "phc": 15}
    # pho group singles = 15, choose 12; phc single 20, choose 15 => 27
    assert minCostBuyAllWords(words, wordCost, bundleCost2) == 27

    # 3) Nested prefixes: 4-letter bundles inside 3-letter group
    bundleCost3 = {
        "pho": 12,
        "phot": 3,   # covers photo only
        "phoe": 10,  # covers phoeo only
        "phos": 100, # covers phose only (too expensive)
        "phc": 15,
        "phce": 8,   # covers phcertd cheaper
    }
    # pho: min(12, 3 + 6 + 4 = 13) => 12
    # phc: min(15, 8) => 8
    # total = 20
    assert minCostBuyAllWords(words, wordCost, bundleCost3) == 20

    # 4) Word is prefix of another word
    words4 = ["a", "ab", "abc"]
    wordCost4 = {"a": 5, "ab": 6, "abc": 7}
    bundleCost4 = {"a": 10, "ab": 3}
    # best: buy "ab" bundle = 3 (covers ab, abc) + buy "a" single = 5 => 8
    assert minCostBuyAllWords(words4, wordCost4, bundleCost4) == 8

    # 5) Bundle equals single sum -> either is fine, min same
    words5 = ["aa", "ab"]
    wordCost5 = {"aa": 4, "ab": 6}
    bundleCost5 = {"a": 10}
    assert minCostBuyAllWords(words5, wordCost5, bundleCost5) == 10

    # 6) Useless bundle (prefix matches no word path) should be ignored
    words6 = ["cat", "car"]
    wordCost6 = {"cat": 7, "car": 5}
    bundleCost6 = {"dog": 1, "ca": 20}
    # "dog" ignored, "ca" too expensive => buy singles: 12
    assert minCostBuyAllWords(words6, wordCost6, bundleCost6) == 12

    # 7) Deep bundle wins (covers multiple words under it)
    words7 = ["abcd", "abce", "abcf", "ax"]
    wordCost7 = {"abcd": 5, "abce": 5, "abcf": 5, "ax": 100}
    bundleCost7 = {"abc": 9, "a": 50}
    # For "abc" subtree: 9 vs 15 => 9, plus "ax" is 100, compare with bundle "a"=50
    # If buy "a" bundle => 50 (covers everything) which is best
    assert minCostBuyAllWords(words7, wordCost7, bundleCost7) == 50

    # 8) Single-character bundle
    words8 = ["x", "xy", "xyz"]
    wordCost8 = {"x": 10, "xy": 10, "xyz": 10}
    bundleCost8 = {"x": 15, "xy": 12}
    # xy covers xy+xyz for 12, plus x single 10 => 22 vs x bundle 15 => choose 15
    assert minCostBuyAllWords(words8, wordCost8, bundleCost8) == 15

    print("All tests passed!")


if __name__ == "__main__":
    runTests()

# ===== END FILE: Uber/MinimumCostBuyAllWordswithPrefixBundles.py =====

# ===== BEGIN FILE: Uber/SubstringWrapper.py =====

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


# ===== END FILE: Uber/SubstringWrapper.py =====

# ===== BEGIN FILE: Uber/WordSearchInStraightLine.py =====

"""
Given an m x n grid of characters board and a string word, return true if word exists in the grid.
The word can be constructed from letters in sequentially adjacent cells, where "adjacent" cells are those horizontally, 
vertically, or diagonally neighboring.
The word must be formed by characters that all lie in a straight line. Once a starting cell and a direction are chosen, 
the path cannot change direction.

Constraints:

1 ≤ m, n ≤ 100
1 ≤ word.length ≤ 100
board and word consist of lowercase English letters.
"""
def wordSearch(board, word):
    if not board or not board[0]:
        return False
    
    numRows = len(board)
    numCols = len(board[0])
    wordLen = len(word)

    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for r in range(numRows):
        for c in range(numCols):
            if board[r][c] == word[0]:
                for dr, dc in DIRS:
                    found = True
                    for k in range(1, wordLen):
                        nr, nc = r + k * dr, c + k * dc

                        if not (0 <= nr < numRows and 0 <= nc < numCols and board[nr][nc] == word[k]):
                            found = False
                            break
                    
                    if found:
                        return True
    
    return False

def runTests():

    board1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f'],
        ['g', 'h', 'i'],
    ]
    assert wordSearch(board1, "abc") is True          # horizontal right
    assert wordSearch(board1, "cba") is True          # horizontal left
    assert wordSearch(board1, "adg") is True          # vertical down
    assert wordSearch(board1, "gda") is True          # vertical up
    assert wordSearch(board1, "aei") is True          # diagonal down-right
    assert wordSearch(board1, "iea") is True          # diagonal up-left
    assert wordSearch(board1, "ceg") is True          # diagonal down-left
    assert wordSearch(board1, "gec") is True          # diagonal up-right

    assert wordSearch(board1, "abe") is False         # not a straight line
    assert wordSearch(board1, "abf") is False         # would require direction change
    assert wordSearch(board1, "abcd") is False        # out of bounds

    board2 = [['a']]
    assert wordSearch(board2, "a") is True
    assert wordSearch(board2, "b") is False

    board3 = [
        ['a', 'a', 'a', 'a'],
        ['a', 'b', 'c', 'a'],
        ['a', 'd', 'e', 'a'],
        ['a', 'a', 'a', 'a'],
    ]
    assert wordSearch(board3, "abc") is True          # b->c is right, starts at (1,1)
    assert wordSearch(board3, "bde") is False         # not collinear
    assert wordSearch(board3, "ae") is True           # diagonal a(0,0)->e(2,2)

    print("All tests passed!")


runTests()



# ===== END FILE: Uber/WordSearchInStraightLine.py =====

# ===== BEGIN FILE: Uber/currencyExchange.py =====

"""
Best Currency Exchange Rate
You are given exchange rates between currencies.
fromArr[i] -> toArr[i] has rate rateArr[i]

Rates work both ways:
if A -> B = r, then B -> A = 1 / r
You can convert through multiple currencies.
A path A -> X -> Y -> B has rate = (A->X) * (X->Y) * (Y->B)

Task
For each query (from, to), return the maximum exchange rate you can get by choosing the best path.
If from or to doesn’t exist, or no path connects them, return -1.0.

Implement
CurrencyConverter(fromArr, toArr, rateArr)
build the converter
getBestRate(from, to) -> double

return best rate from from to to

Example
Rates:
GBP -> JPY = 155
USD -> JPY = 112
USD -> GBP = 0.9

Query: USD -> JPY
Direct: 112
Indirect: USD -> GBP -> JPY = (1/0.9) * 155 = 139.5
Answer: 139.5
"""
from collections import defaultdict
class CurrencyConverter:
    def __init__(self, fromArr, toArr, rateArr):
        self.g = defaultdict(list)

        for a, b,r in zip(fromArr, toArr, rateArr):
            self.g[a].append((b, r))
            self.g[b].append((a, 1.0 / r))
    
    def getBestRate(self, fromCurrency, toCurrency):
        if fromCurrency not in self.g or toCurrency not in self.g:
            return -1.0
        
        if fromCurrency == toCurrency:
            return 1.0
        
        visited = set()

        def dfs(cur, rateSoFar):
            if cur == toCurrency:
                return rateSoFar

            visited.add(cur)
            best = -1.0

            for nxt, r in self.g[cur]:
                if nxt in visited:
                    continue
                best = max(best, dfs(nxt, rateSoFar*r))
            
            visited.remove(cur)
            return best

        return dfs(fromCurrency, 1.0)
    
def runTests():
    # Example from prompt
    fromArr = ["GBP", "USD", "USD", "USD", "CNY"]
    toArr   = ["JPY", "JPY", "GBP", "CAD", "EUR"]
    rateArr = [155.0, 112.0, 0.9, 1.3, 0.14]

    cc = CurrencyConverter(fromArr, toArr, rateArr)

    # 1) Better indirect path
    assert abs(cc.getBestRate("USD", "JPY") - 139.5) < 1e-9

    # 2) Reverse direction via inverse edges:
    # JPY -> USD = 1/112, USD -> GBP = 0.9  => 0.9/112
    assert abs(cc.getBestRate("JPY", "GBP") - (0.9 / 112.0)) < 1e-12

    # 3) Currency not present
    assert cc.getBestRate("XYZ", "GBP") == -1.0

    # 4) No path exists (CNY only connects to EUR)
    assert cc.getBestRate("CNY", "CAD") == -1.0

    # 5) Same currency
    assert cc.getBestRate("USD", "USD") == 1.0

    # Extra: direct beats indirect
    fromArr2 = ["A", "B", "A"]
    toArr2   = ["B", "C", "C"]
    rateArr2 = [2.0, 2.0, 10.0]  # A->C direct is 10, indirect A->B->C is 4
    cc2 = CurrencyConverter(fromArr2, toArr2, rateArr2)
    assert abs(cc2.getBestRate("A", "C") - 10.0) < 1e-9

    # Extra: indirect beats direct
    fromArr3 = ["A", "A", "B"]
    toArr3   = ["C", "B", "C"]
    rateArr3 = [3.0, 2.0, 2.0]   # A->C direct is 3, indirect A->B->C is 4
    cc3 = CurrencyConverter(fromArr3, toArr3, rateArr3)
    assert abs(cc3.getBestRate("A", "C") - 4.0) < 1e-9

    print("All tests passed!")


runTests()


# ===== END FILE: Uber/currencyExchange.py =====

# ===== BEGIN FILE: templates/Floyd.py =====

from typing import List

def shortestPathFloyd(graph: List[List[int]]) -> List[List[int]]:
    n = len(graph)  # Number of nodes
    dist = [[float('inf')] * n for i in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u in range(n):  # For each node
        for v in graph.get(u, []):
            dist[u][v] = 1

    for k in range(n):  # k is intermediate node
        for i in range(n):
            for j in range(n):
                # Update the distance if a shorter path is found
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# ===== END FILE: templates/Floyd.py =====

# ===== BEGIN FILE: templates/Kruskal.py =====

import Unionfind

def kruskal(n, edges):
    uf = Unionfind(n)
    mst = []
    edges.sort(key=lambda x: x[2])  # Sort edges by weight
    for u, v, weight in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
    return mst

# ===== END FILE: templates/Kruskal.py =====

# ===== BEGIN FILE: templates/LazyHeap.py =====

from collections import defaultdict
from heapq import heappop, heappush, heappushpop
from math import inf
"""
A LazyHeap implementation using Python's heapq and a lazy deletion strategy.

Classes:
    LazyHeap: A min-heap supporting efficient lazy removal of arbitrary elements.

Methods:
    __init__():
        Initializes an empty LazyHeap.

    remove(num: int) -> None:
        Marks the given number for removal from the heap. The actual removal is deferred until the number reaches the top of the heap.

    applyRemove() -> None:
        Removes all elements from the top of the heap that have been marked for removal.

    push(num: int) -> None:
        Pushes a number onto the heap.

    top() -> int:
        Returns the smallest element in the heap, applying any pending removals.

    pop() -> int:
        Removes and returns the smallest element in the heap, applying any pending removals.

    pushPop(num: int) -> int:
        Pushes a number onto the heap and then pops and returns the smallest element, applying any pending removals.
"""

class LazyHeap:
    def __init__(self):
        self.hp = []
        self.lazy = defaultdict(int) # record the item not deleted yet
        self.size = 0

    # tag the target num to be removed
    def remove(self, num: int) -> None:
        self.lazy[num] += 1
        self.size -= 1

    # pop all nums at top which has been tagged
    def applyRemove(self) -> None:
        while self.hp and self.lazy[self.hp[0]] > 0:
            self.lazy[self.hp[0]] -= 1
            heappop(self.hp)

    def push(self, num: int) -> None:
        heappush(self.hp, num)

    # check the top of heap
    def top(self) -> int:
        self.applyRemove()
        return self.hp[0]

    def pop(self) -> int:
        self.applyRemove()
        self.size -= 1
        return heappop(self.hp)

    def pushPop(self, num: int) -> int:
        self.applyRemove()
        return heappushpop(self.hp, num)









# ===== END FILE: templates/LazyHeap.py =====

# ===== BEGIN FILE: templates/OOP_fundamentals.py =====

from enum import Enum
import threading

class OrderStatus(Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"



status = OrderStatus.PLACED

if status == OrderStatus.PLACED:
    print("Order has been placed.")


from abc import ABC, abstractmethod

# interface of PaymentGateway, it is an abstract base class
class PaymentGateway(ABC):
    @abstractmethod
    def initiate_payment(self, amount):
        pass

# implementation of PaymentGateway
class StripePaymentGateway(PaymentGateway):
    def initiate_payment(self, amount):
        print(f"Initiating payment of ${amount} through Stripe.")
# implementation of PaymentGateway
class PayPalPaymentGateway(PaymentGateway):
    def initiate_payment(self, amount):
        print(f"Initiating payment of ${amount} through PayPal.")


# abstraction
class Vehicle(ABC):
    def __init__(self, brand):
        self.brand = brand
    
    @abstractmethod
    def drive(self):
        pass

# inheritance
class Car(Vehicle):
    def __init__(self, brand):
        super().__init__(brand)
    
    def drive(self):
        print(f"Driving a {self.brand} car.")
    

# unidirectional association
class PaymentGateway:
    def process_payment(self, amount: float):
        pass 
class Order:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

# assiociation bidirectional
class Developer:
    def __init__(self):
        self.team = None 
    
    def set_team(self, team):
        self.team = team 

class Team:
    def __init__(self):
        self.developers = []
    
    def add_developer(self, dev: Developer):
        self.developers.append(dev)
        dev.set_team(self)

# one-to-one association
class Profile:
    def __init__(self):
        self.user = None
    
    def set_user(self, user):
        self.user = user

class User:
    def __init__(self):
        self.profile = None
    
    def set_profile(self, profile):
        self.profile = profile
        profile.set_user(self)


# one-to-many association
class Issue:
    def __init__(self):
        self.project = None 
    
    def set_project(self, project):
        self.project = project

class Project:
    def __init__(self):
        self.issues = []
    
    def add_issue(self, issue: Issue):
        self.issues.append(issue)
        issue.set_project(self)


# aggregation

class Professor:
    def __init__(self, name):
        self.name = name 
    
    def get_name(self):
        return self.name 
    
class Department:
    def __init_(self, name, professors):
        self.name = name
        self.professors = professors
    
    def print_professors(self):
        print("Professors in the department:")
        for professor in self.professors:
            print(professor.get_name())

        


# Dependency, short-lived; no ownership; Uses-a relationship

class Document:
    def __init__(self, content):
        self.content = content
    
    def get_content(self):
        return self.content

class Printer:
    def print(self, document):
        print(document.get_content())

# Dependency injection
#interface
class Sender(ABC):
    @abstractmethod
    def send(self, message) -> None:
        pass 


class NotificationService:
    def __init__(self, sender: Sender):
        self.sender = sender 
    
    def notify_user(self, message):
        self.sender.send(message)



# design pattern

## Singleton pattern
class LazySingleton:
    _instance = None

    def __init__(self):
        if LazySingleton._instance is not None:
            raise Exception("This class is a singleton!")
    
    @staticmethod
    def get_instance():
        if LazySingleton._instance is None:
            LazySingleton._instance = LazySingleton()
        return LazySingleton._instance

# thread-safe Singleton pattern
class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if ThreadSafeSingleton._instance is not None:
            raise Exception("This class is a singleton!")
    
    @staticmethod
    def get_instance():
        with ThreadSafeSingleton._lock:
            if ThreadSafeSingleton._instance is None:
                ThreadSafeSingleton._instance = ThreadSafeSingleton()
        return ThreadSafeSingleton._instance

# Factory pattern

class SimpleNotificationFactory:
    @staticmethod
    def create_notification(type):
        match type:
            case 'EMAIL':
                return EmailNotification()
            case 'SMS':
                return SMSNotification()
            case 'PUSH':
                return PushNotification()
            case _:
                raise ValueError("Invalid notification type")
# core logic focused. It only uses the notification, it doesn't construct it.
class NotificationService:
    def send_notification(self, type, message):
        notification = SimpleNotificationFactory.create_notification(type)
        notification.send(message)


# Factory method pattern
class Notification(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailNotification(Notification):
    def send(self, message):
        print(f"Sending email notification with message: {message}")

class SMSNotification(Notification):
    def send(self, message):
        print(f"Sending SMS notification with message: {message}")

class PushNotification(Notification):
    def send(self, message):
        print(f"Sending push notification with message: {message}")

# Defind an abstract creator
class NotificationCreator(ABC):
    @abstractmethod
    def create_notification(self):
        pass

    def send(self, message):
        Notification = self.create_notification()
        Notification.send(message)



class EmailNotificationCreator(NotificationCreator):
    def create_notification(self):
        return EmailNotification()
    
# now I want to create slack notification
class SlackNotification(Notification):
    def send(self, message):
        print(f"Sending slack notification with message: {message}")

class SlackNotificationCreator(NotificationCreator):
    def create_notification(self):
        return SlackNotification()

# ===== END FILE: templates/OOP_fundamentals.py =====

# ===== BEGIN FILE: templates/SegmentTree.py =====

# dynamic node segment tree
# range update | range query (min, max, sum)
class SegmentTreeNode:
    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.left = None # son node
        self.right = None # son node
        self.sum = 0
        self.min = 0
        self.max = 0
        self.lazy = 0

class SegmentTree:
    def __init__(self, l, r):
        self.root = SegmentTreeNode(l, r)

    def push(self, node): # push down value
        if node.lazy != 0 and node.l != node.r: # have value need to push, and has son nodes
            if not node.left:
                m = (node.l + node.r) // 2
                node.left = SegmentTreeNode(node.l, m)
                node.right = SegmentTreeNode(m+1, node.r)
            for child in [node.left, node.right]:
                child.lazy += node.lazy
                child.sum += (child.r - child.l + 1) * node.lazy
                child.min += node.lazy
                child.max += node.lazy
            node.lazy = 0

    def update(self, node, l, r, val): # add val to range [l, r]
        if node.r < l or node.l > r: # no overlap
            return

        if l <= node.l and node.r <= r: # completely overlap
            node.sum += (node.r - node.l + 1) * val
            node.min += val
            node.max += val
            node.lazy += val
            return

        self.push(node) # push val down before dive deep

        m = (node.l + node.r) // 2
        if not node.left:
            node.left = SegmentTreeNode(node.l, m)
        if not node.right:
            node.right = SegmentTreeNode(m + 1, node.r)

        self.update(node.left, l, r, val)
        self.update(node.right, l, r, val)

        node.sum = node.left.sum + node.right.sum
        node.min = min(node.left.min, node.right.min)
        node.max = max(node.left.max, node.right.max)

    def query_sum(self, node, l, r):
        if not node or node.r < l or node.l > r:
            return 0
        if l <= node.l and node.r <= r:
            return node.sum
        self.push(node)
        return self.query_sum(node.left, l, r) + self.query_sum(node.right, l, r)

    def query_min(self, node, l, r):
        if not node or node.r < l or node.l > r:
            return float('inf')
        if l <= node.l and node.r <= r:
            return node.min
        self.push(node)
        return min(self.query_min(node.left, l, r), self.query_min(node.right, l, r))

    def query_max(self, node, l , r):
        if not node or node.r < l or node.l > r:
            return float('-inf')
        if l <= node.l and node.r <= r:
            return node.max
        self.push(node)
        return max(self.query_max(node.left, l, r), self.query_max(node.right, l, r))

# Example usage:
def main():
    st = SegmentTree(0, 100000)
    st.update(st.root, 1, 10, 5)
    print("Sum [1,4]:", st.query_sum(st.root, 1, 4))
    print("Min [2,3]:", st.query_min(st.root, 2, 3))
    print("Max [5,7]:", st.query_max(st.root, 5, 7))

if __name__ == "__main__":
    main()


# ===== END FILE: templates/SegmentTree.py =====

# ===== BEGIN FILE: templates/Unionfind.py =====

class UnionFind:
    def __init__(self, n):
        self.root = [i for i in range(n)]
        self.size = [1 for _ in range(n)]
        self.group_count = n

    def find(self, x) -> int:
        if x == self.root[x]:
            return x
        # path compression
        self.root[x] = self.find(self.root[x])
        return self.root[x]
    # Union two elements
    def union(self, a, b) -> bool:
        pa, pb = self.find(a), self.find(b)
        if pa == pb:
            return False
        
        if self.size[pa] < self.size[pb]:
            pa, pb = pb, pa
        
        self.root[pb] = pa
        self.size[pa] += self.size[pb]
        self.group_count -= 1
        return True

    # Check if two elements are in the same group
    def query(self, a, b) -> bool:
        return self.find(a) == self.find(b)

    # Get the number of disjoint groups
    def groups(self) -> int:
        return self.group_count

# ===== END FILE: templates/Unionfind.py =====

# ===== BEGIN FILE: templates/bipartie.py =====

from typing import List
# method 1: BFS
def isBipartiteBFS(graph: List[List[int]]) -> bool:
    color = {}
    for start in range(len(graph)):
        if start not in color:
            queue = [start]
            color[start] = 0
            while queue:
                tmp = queue[:]
                queue = []
                for node in tmp:
                    for neighbor in graph.get(node, []):
                        if neighbor not in color:
                            color[neighbor] = 1 - color[node]
                            queue.append(neighbor)
                        elif color[neighbor] == color[node]:
                            return False
    return True

# method 2: DFS
def isBipartiteDFS(graph: List[List[int]]) -> bool:
    color = {}
    def dfs(node: int, c: int) -> bool:
        if node in color:
            return color[node] == c
        color[node] = c
        for neighbor in graph.get(node, []):
            if not dfs(neighbor, 1 - c):
                return False
        return True
    for start in range(len(graph)):
        if start not in color and not dfs(start, 0):
            return False
    return True

# method 3: Union-Find
import Unionfind   
def isBipartiteUnionFind(graph: List[List[int]]) -> bool:
    uf = Unionfind.UnionFind(len(graph))
    for node in range(len(graph)):
        for neighbor in graph.get(node, []):
            if uf.find(node) == uf.find(neighbor):
                return False
            uf.union(uf.find(node), uf.find(neighbor))
    return True


# ===== END FILE: templates/bipartie.py =====

# ===== BEGIN FILE: templates/pow_mul.py =====

# a @ b @ is matrix multiple
from typing import List

MOD = 10**9 + 7


# multiply two matrices with all entries taken modulo MOD
def mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [[sum(x*y for x, y in zip(row, col)) % MOD for col in zip(*b)] for row in a]



# a^n @ f1
# fast exponentiation of matrix `a` applied to `f1`, with all ops modulo MOD
def pow_mul(a: List[List[int]], n: int, f1: List[List[int]]) -> List[List[int]]:
    res = f1
    while n:
        if n & 1:
            res = mul(a, res)
        a = mul(a, a)
        n >>= 1
    return res


# ===== END FILE: templates/pow_mul.py =====

# ===== BEGIN FILE: templates/test_lazyHeap.py =====

import unittest
from LazyHeap import LazyHeap

class TestLazyHeapApplyRemove(unittest.TestCase):
    def test_apply_remove_no_lazy(self):
        heap = LazyHeap()
        heap.push(1)
        heap.push(2)
        heap.push(3)
        heap.applyRemove()
        self.assertEqual(heap.hp, [1, 2, 3])

    def test_apply_remove_single(self):
        heap = LazyHeap()
        heap.push(1)
        heap.push(2)
        heap.push(3)
        heap.remove(1)
        heap.applyRemove()
        self.assertEqual(heap.hp, [2, 3])
        self.assertEqual(heap.lazy[1], 0)

    def test_apply_remove_multiple(self):
        heap = LazyHeap()
        for num in [1, 2, 2, 3]:
            heap.push(num)
        heap.remove(1)
        heap.remove(2)
        heap.applyRemove()
        # Only one '2' should be removed, one remains
        self.assertEqual(heap.hp, [2, 3])
        self.assertEqual(heap.lazy[1], 0)
        self.assertEqual(heap.lazy[2], 0)

    def test_apply_remove_all_lazy_at_top(self):
        heap = LazyHeap()
        for num in [1, 1, 2, 3]:
            heap.push(num)
        heap.remove(1)
        heap.remove(1)
        heap.applyRemove()
        self.assertEqual(heap.hp, [2, 3])
        self.assertEqual(heap.lazy[1], 0)

    def test_apply_remove_lazy_not_at_top(self):
        heap = LazyHeap()
        for num in [2, 3, 1]:
            heap.push(num)
        heap.remove(3)
        heap.applyRemove()
        # 3 is not at the top, so nothing should be removed
        self.assertEqual(sorted(heap.hp), [1, 2, 3])
        self.assertEqual(heap.lazy[3], 1)

if __name__ == "__main__":
    unittest.main()

# ===== END FILE: templates/test_lazyHeap.py =====

