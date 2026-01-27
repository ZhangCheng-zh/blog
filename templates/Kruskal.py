import Unionfind

def kruskal(n, edges):
    uf = Unionfind(n)
    mst = []
    edges.sort(key=lambda x: x[2])  # Sort edges by weight
    for u, v, weight in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
    return mst