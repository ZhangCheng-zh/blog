from collections import defaultdict
from heapq import heappop, heappush, heappushpop
from math import inf
"""
A LazyHeap implementation using Python's heapq and a lazy deletion strategy.

Classes:
    LazyHeap: A min-heap supporting efficient lazy removal of arbitrary elements.

Methods:
    __init__():
        Initializes an empty LazyHeap.

    remove(num: int) -> None:
        Marks the given number for removal from the heap. The actual removal is deferred until the number reaches the top of the heap.

    applyRemove() -> None:
        Removes all elements from the top of the heap that have been marked for removal.

    push(num: int) -> None:
        Pushes a number onto the heap.

    top() -> int:
        Returns the smallest element in the heap, applying any pending removals.

    pop() -> int:
        Removes and returns the smallest element in the heap, applying any pending removals.

    pushPop(num: int) -> int:
        Pushes a number onto the heap and then pops and returns the smallest element, applying any pending removals.
"""

class LazyHeap:
    def __init__(self):
        self.hp = []
        self.lazy = defaultdict(int) # record the item not deleted yet
        self.size = 0

    # tag the target num to be removed
    def remove(self, num: int) -> None:
        self.lazy[num] += 1
        self.size -= 1

    # pop all nums at top which has been tagged
    def applyRemove(self) -> None:
        while self.hp and self.lazy[self.hp[0]] > 0:
            self.lazy[self.hp[0]] -= 1
            heappop(self.hp)

    def push(self, num: int) -> None:
        heappush(self.hp, num)

    # check the top of heap
    def top(self) -> int:
        self.applyRemove()
        return self.hp[0]

    def pop(self) -> int:
        self.applyRemove()
        self.size -= 1
        return heappop(self.hp)

    def pushPop(self, num: int) -> int:
        self.applyRemove()
        return heappushpop(self.hp, num)







