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
