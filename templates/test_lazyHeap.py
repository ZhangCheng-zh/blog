import unittest
from LazyHeap import LazyHeap

class TestLazyHeapApplyRemove(unittest.TestCase):
    def test_apply_remove_no_lazy(self):
        heap = LazyHeap()
        heap.push(1)
        heap.push(2)
        heap.push(3)
        heap.applyRemove()
        self.assertEqual(heap.hp, [1, 2, 3])

    def test_apply_remove_single(self):
        heap = LazyHeap()
        heap.push(1)
        heap.push(2)
        heap.push(3)
        heap.remove(1)
        heap.applyRemove()
        self.assertEqual(heap.hp, [2, 3])
        self.assertEqual(heap.lazy[1], 0)

    def test_apply_remove_multiple(self):
        heap = LazyHeap()
        for num in [1, 2, 2, 3]:
            heap.push(num)
        heap.remove(1)
        heap.remove(2)
        heap.applyRemove()
        # Only one '2' should be removed, one remains
        self.assertEqual(heap.hp, [2, 3])
        self.assertEqual(heap.lazy[1], 0)
        self.assertEqual(heap.lazy[2], 0)

    def test_apply_remove_all_lazy_at_top(self):
        heap = LazyHeap()
        for num in [1, 1, 2, 3]:
            heap.push(num)
        heap.remove(1)
        heap.remove(1)
        heap.applyRemove()
        self.assertEqual(heap.hp, [2, 3])
        self.assertEqual(heap.lazy[1], 0)

    def test_apply_remove_lazy_not_at_top(self):
        heap = LazyHeap()
        for num in [2, 3, 1]:
            heap.push(num)
        heap.remove(3)
        heap.applyRemove()
        # 3 is not at the top, so nothing should be removed
        self.assertEqual(sorted(heap.hp), [1, 2, 3])
        self.assertEqual(heap.lazy[3], 1)

if __name__ == "__main__":
    unittest.main()