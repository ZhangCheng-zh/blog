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