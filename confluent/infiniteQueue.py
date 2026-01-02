"""
An infinite queue is a data structure that dynamically expands to hold an unlimited number of elements. Implement an infinite queue specifically for integers, supporting the following operations:

offer(int val): Add an integer to the tail of the queue.
int poll(): Removes and returns the integer at the front of the queue. If the queue is empty, returns -1.
int getRandom(): Returns a random integer from the queue. If the queue is empty, returns -1.
All operations must be implemented to run in O(1) time.

Constraints:

The number of operations will not exceed 105.
All integers are within the range [-109, 109].
Example 1:

Input:
["InfiniteQueue", "offer", "offer", "offer", "offer", "offer", "getRandom", "getRandom", "getRandom", "poll", "poll", "poll", "poll", "poll"]
[[], [1], [2], [3], [4], [5], [], [], [], [], [], [], [], []]

Output:
[null, null, null, null, null, null, 3, 1, 5, 1, 2, 3, 4, 5]
"""

import random


class InfiniteQueue:
    """
    Infinite (dynamically growing) integer queue with:
      - offer: append to tail
      - poll: pop from head
      - getRandom: random element from current queue
    All in O(1) time (amortized), O(n) space.
    """

    def __init__(self):
        self.cap = 4
        self.buf = [0] * self.cap
        self.head = 0
        self.size = 0
    def _size(self, newCap) -> None:
        return

    def offer(self, val) -> None:
        if self.size == self.cap:
            self._resize(self.cap * 2)
        
        tail = (self.head + self.size) % self.cap
        self.buf[tail] = val
        self.size += 1

    def poll(self) -> int:
        if self.size == 0:
            return -1
        val = self.buf[self.head]
        self.head = (self.head + 1) % self.cap
        self.size -= 1

        if self.cap > 4 and self.size <= self.cap // 4:
            self._resize(self.cap // 2)
        
        return val
    def getRandom(self) -> int:
        if self.size == 0:
            return -1
        
        k = random.randrange(self.size)

        return self.buf[(self.head + k) % self.cap]
        
    def _resize(self, newCap):
        newBuf = [0] * newCap
        for i in range(self.size):
            newBuf[i] = self.buf[(self.head + i) % self.cap]
        
        self.buf = newBuf
        self.cap = newCap
        self.head = 0


if __name__ == "__main__":
    queue = InfiniteQueue()
    queue.offer(1)
    queue.offer(2)
    queue.offer(3)
    queue.offer(4)
    queue.offer(5)

    print("Below are random outputs:")
    print(queue.getRandom())
    print(queue.getRandom())
    print(queue.getRandom())
    print("Below are fixed outputs:")
    print(queue.poll())  # 1
    print(queue.poll())  # 2
    print(queue.poll())  # 3
    print(queue.poll())  # 4
    print(queue.poll())  # 5
    print(queue.poll())  # -1
