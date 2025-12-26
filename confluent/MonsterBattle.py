"""
A -> B means A can defeat B
Input:
1 monsters: dragons, zombies, snakes, goblins, ......
dragons -> zombies, goblins
zombies -> goblins
goblins -> snakes

output:
The least-strong monster that can defeat every monster in the input list([snakes, goblins]).
(eg. in this case it's zombie, because a dragon is more powerful)

if there are multiple answers, you can return any of them.
"""

from collections import defaultdict, deque
from typing import List

def findLeastStrongDefenders(monsters: dict[List[str]], hostile_list: List[str]):
    # monsters: dict[str -> monsters(list)]
    # step 1 build reverse graph
    rg = defaultdict(set)
    for name, m in monsters.items():
        for defeated in m:
            rg[defeated].add(name)
        
    # find all who can defeat target
    def bfs(target):
        q = [target]
        visited = set()
        visited.add(target)
        while q:
            tmp = q[:]
            q = []
            for target in tmp:
                for attacker in rg[target]:
                    if attacker not in visited:
                        visited.add(attacker)
                        q.append(attacker)
        return visited

    # find monsters that in all visited
    hostileSet = hostile_list[:]
    ans = None
    for target in hostile_list:
        mons = bfs(target)
        if not ans:
            ans = mons
        else:
            ans &= mons
    
    if not ans: return [] # not monster can beat all hostile

    # remove hostile monster in ans:
    ans = {m for m in ans if m not in hostile_list}

    # remove monster whose any ancestors is also in ans
    def remove_ancestors(cur, has_defender_above):
        

    

