"""
Implement the LRUCache class:

LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
int get(int key) Return the value of the key if the key exists, otherwise return -1.
void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.
The functions get and put must each run in O(1) average time complexity.

Example 1:

Input
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
Output
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4
 

Constraints:

1 <= capacity <= 3000
0 <= key <= 104
0 <= value <= 105
At most 2 * 105 calls will be made to get and put.
"""
from collections import defaultdict
from typing import Optional
import math
inf = math.inf

class CacheNode:
    def __init__(self, key: int, value: int, prev: Optional['CacheNode'] = None, next: Optional['CacheNode'] = None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next
        

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # use a hashmap and double linked list to save the LRU cache
        self.hm = {}
        # create a dummy node for double linked list
        self.dllist = self.dummy = CacheNode(inf, inf)
        # make dllist be a circle, easy to reach tail
        self.dummy.prev = self.dummy.next = self.dummy

    def delTail(self):
        tail = self.dummy.prev
        
        tail.prev.next = tail.next
        tail.next.prev = tail.prev

        return tail

    def delNode(self, node: CacheNode):
        prev = node.prev 
        next = node.next

        prev.next = next 
        next.prev = prev

    
    def insertHead(self, node: CacheNode):
        prev = self.dummy
        next = self.dummy.next

        node.prev = prev
        prev.next = node
        node.next = next
        next.prev = node
    

    def get(self, key: int):
        # print('before get')
        # print('hm', self.hm.keys())
        # print('target key:', key)
        # if key in map
        # first pick out the node
        # then put it into head
        if key in self.hm:
            targetNode = self.hm[key]
            self.delNode(targetNode)
            self.insertHead(targetNode)
            return targetNode.value
        return -1

    def put(self, key: int, value: int):
        # if key not exist
        if key not in self.hm:
            # if size reach capacity, delete tail node
            if len(self.hm) == self.capacity:
                delNode = self.delTail()
                del self.hm[delNode.key]

            # create a new node
            self.hm[key] = newNode = CacheNode(key, value)

            # put the node into head of dllist
            self.insertHead(newNode)


        # if key already exist
        targetNode = self.hm[key]
        # pick out the target key
        self.delNode(targetNode)
        # update value
        targetNode.value = value
        # put it into head of dllist
        self.insertHead(targetNode)

        # print('after put')
        # print('hm', self.hm.keys())
        # print('dllist')
        # hd = self.dllist.next
        # while hd is not self.dummy:
        #     print(hd.key)
        #     hd = hd.next
        return