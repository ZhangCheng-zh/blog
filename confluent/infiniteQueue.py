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
# a infinite queue for integers
class InfiniteQueue:
    def __init__(self):
        self.capacity = 4 # when all used, double the size, when usage down to 1/4 size, shrink capacity to half
        self.size = 0
        self.buf = [0] * self.capacity
        self.head = 0
    
    def _resize(self, newCapacity):
        newBuf = [0] * newCapacity
        
        for i in range(self.size):
            newBuf[i] = self.buf[(self.head + i) % self.capacity]
        
        self.buf = newBuf
        self.capacity = newCapacity
        self.head = 0



    # add an integer to the tail of the queue
    def offer(self, val): # time: O(1)
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        
        tail = (self.head + self.size) % self.capacity 
        self.buf[tail] = val
        self.size += 1

    # removes and returns the integer at the front of the queue.
    def poll(self): # time: O(1)
        if self.size == 0:
            return -1

        val = self.buf[self.head]
        self.head = (self.head + 1) % self.capacity 
        self.size -= 1

        if self.capacity > 4 and self.size <= self.capacity // 4:
            self._resize(self.capacity // 2) 
        
        return val

    # return a random integer from the queue
    def getRandom(self): # time: O(1)
        if self.size == 0:
            return -1
        # random.random return float
        # below can use random.randint(0, size - 1)
        k = random.randrange(self.size)

        return self.buf[(self.head + k) % self.capacity]

import random


# basic offer/poll order
q = InfiniteQueue()
q.offer(1); q.offer(2); q.offer(3)
assert q.poll() == 1
assert q.poll() == 2
assert q.poll() == 3
assert q.poll() == -1  # empty

# wrap-around without resize
q = InfiniteQueue()
q.offer(10); q.offer(20); q.offer(30); q.offer(40)
assert q.poll() == 10
assert q.poll() == 20
q.offer(50); q.offer(60)  # should wrap in buffer
assert q.poll() == 30
assert q.poll() == 40
assert q.poll() == 50
assert q.poll() == 60
assert q.poll() == -1

# grow (forces resize up)
q = InfiniteQueue()
for i in range(1, 9):  # > initial capacity 4
    q.offer(i)
for i in range(1, 9):
    assert q.poll() == i
assert q.poll() == -1

# getRandom returns an element in queue
q = InfiniteQueue()
q.offer(7); q.offer(8); q.offer(9)
random.seed(0)
x = q.getRandom()
assert x in (7, 8, 9)

# getRandom on empty
q = InfiniteQueue()
assert q.getRandom() == -1
