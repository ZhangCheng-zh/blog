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