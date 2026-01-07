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





        
    