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
