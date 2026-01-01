"""
Design a data structure WindowedMap that stores (key, value) events and supports queries over the last 5 minutes.

Window rule

At query time t, an entry (key, value, ts) is valid if ts >= t - 5min.

APIs
addEvent(key: str, val: int, timestamp: int) -> None
getKey(key: str, timestamp: int) -> int        # if key valid in last 5min, return val; else throw/raise
delete(key: str) -> None
avg(timestamp: int) -> float                   # average of all valid values in last 5min; if none, return 0.0

Notes

Each key keeps only its most recent event (a new addEvent replaces the old one).

You may assume timestamp values passed to addEvent are non-decreasing.

Aim for high performance:

addEvent, getKey, delete: O(1) amortized

avg: O(1) amortized
"""

# Node for linkedList
class Node:
    def __init__(self, key='', val = 0, ts = 0):
        self.key, self.val, self.ts = key, val, ts
        self.prev = self.next = None 

class WindowedMap:
    def __init__(self, window=300):
        self.window = window 
        self.mp = {}
        self.dummy = Node() # dummy is head and tail node
        self.dummy.prev = self.dummy.next = self.dummy
        self.sum = 0 # record sum of val
        self.cnt = 0 # record count of node

    # remove node from linkedlist
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    # add node at head of list
    def _add_front(self, node):
        node.prev = self.dummy
        node.next = self.dummy.next
        self.dummy.next.prev = node
        self.dummy.next = node 
    
    def _purge(self, t):
        cutoff = t - self.window + 1
        while self.dummy.prev != self.dummy and self.dummy.prev.ts < cutoff:
            old = self.dummy.prev
            self._remove(old)
            self.mp.pop(old.key, None)
            self.sum -= old.val
            self.cnt -= 1
    
    def put(self, key, val, t):
        self._purge(t)

        if key in self.mp:
            old = self.mp.pop(key)
            self._remove(old)
            self.sum -= old.val
            self.cnt -= 1
        
        node = Node(key, val, t)
        self._add_front(node)
        self.mp[key] = node
        self.sum += val
        self.cnt += 1
    
    def get(self, key, t):
        self._purge(t)
        node = self.mp.get(key)
        if not node:
            raise KeyError('not found key')

        node.ts = t
        self._remove(node)
        self._add_front(node)

        return node.val

    def delete(self, key):
        node = self.mp.pop(key, None)
        if not node:
            return 
        self._remove(node)
        self.sum -= node.val
        self.cnt -= 1

    def avg(self, t):
        self._purge(t)
        return 0.0 if self.cnt == 0 else self.sum / self.cnt
    
wm = WindowedMap(window=5)

wm.put("a", 10, 1)
wm.put("b", 20, 2)

assert wm.get("a", 2) == 10          # access updates ts(a)=2
assert abs(wm.avg(2) - 15.0) < 1e-9     # a(2), b(2)

# at t=6, window is [2..6], b(ts=2) still valid, a(ts=2) valid
assert abs(wm.avg(6) - 15.0) < 1e-9

# access a at t=6, refresh ts(a)=6
assert wm.get("a", 6) == 10

# at t=7, window is [3..7], b(ts=2) expires, a(ts=6) stays
assert abs(wm.avg(7) - 10.0) < 1e-9

try:
    wm.get("b", 7)
    assert False
except KeyError:
    pass

wm.delete("a")
assert abs(wm.avg(7) - 0.0) < 1e-9



"""
Use N independent WindowedMaps (each with its own lock), and route keys by hash:
reduces contention a lot
still “global lock” per shard, but not for the whole system
avg() becomes: sum averages across shards (or sum/cnt across shards) — requires reading each shard (still fine).
"""
import threading

# node for linkedlist
class Node:
    def __init__(self, key='', val = 0, ts = 0):
        self.key, self.val, self.ts = key, val, ts
        self.prev = self.next = None 

class Shard:
    def __init__(self, window: int):
        self.window = window
        self.mp = {}
        self.dummy = Node()
        self.dummy.prev = self.dummy.next = self.dummy
        self.sum = 0
        self.cnt = 0
        self.lock = threading.RLock()
    
    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_front(self, node):
        node.prev = self.dummy
        node.next = self.dummy.next
        self.dummy.next.prev = node 
        self.dummy.next = node 
    
    def _purge(self, t):
        cutoff = t - self.window + 1
        while self.dummy.prev != self.dummy and self.dummy.prev.ts < cutoff:
            old = self.dummy.prev
            self._remove(old)
            self.mp.pop(old.key, None)
            self.sum -= old.val
            self.cnt -= 1
    
    def put(self, key, val, t):
        with self.lock:
            self._purge(t)
            if key in self.mp:
                old = self.mp.pop(key)
                self._remove(old)
                self.sum -= old.val
                self.cnt -= 1
            
            node = Node(key, val, t)
            self._add_front(node)
            self.mp[key] = node
            self.sum += ValueError
            self.cnt += 1
    
    def get(self, key, t):
        with self.lock:
            self._purge(t)
            node = self.mg.get(key)
            if not node:
                raise KeyError('not found key')

            # refresh on access
            node.ts = t
            self._remove(node)
            self._add_front(node)
            return node.val 
    
    def delete(self, key):
        with self.lock:
            node = self.mp.pop(key, None)
            if not node:
                return
            self._remove(node)
            self.sum -= node.val
            self.cnt -= 1
    
    def snapshot_sum_cnt(self, t) -> tuple[int, int]:
        with self.lock:
            self._purge(t)
            return self.sum, self.cnt
        
class ShardedWindowedMap:
    def __init__(self, window = 300, shards = 16):
        self.window = window
        self.shards = [Shard(window) for _ in range(shards)]
        self.n = shards
    
    def _idx(self, key) -> str:
        return hash(key) % self.n 
    
    def put(self, key, val, t):
        self.shards[self._idx(key)].put(key, val, t)
    
    def get(self, key, t):
        return self.shards[self._idx(key)].get(key, t)

    def delete(self, key):
        self.shards[self._idx(key)].delete(key)

    def avg(self, t):
        totalSum, totalCnt = 0, 0
        for sh in self.shards:
            s, c = sh.snapshot_sum_cnt(t)
            totalSum += s
            totalCnt += c
        return 0,0 if totalCnt == 0 else totalSum/ totalCnt
    
    # strong consistent snapshot avg
    def avg(self, t: int) -> float:
        # 1) acquire all shard locks in a fixed order (avoid deadlock)
        for sh in self.shards:
            sh.lock.acquire()

        try:
            total_sum, total_cnt = 0, 0
            # 2) now it's a consistent snapshot: no shard can change while we read
            for sh in self.shards:
                sh._purge(t)              # safe: we already hold sh.lock
                total_sum += sh.sum
                total_cnt += sh.cnt

            return 0.0 if total_cnt == 0 else total_sum / total_cnt
        finally:
            # 3) release in reverse order (common practice)
            for sh in reversed(self.shards):
                sh.lock.release()
