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