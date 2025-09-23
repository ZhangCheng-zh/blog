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
