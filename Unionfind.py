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