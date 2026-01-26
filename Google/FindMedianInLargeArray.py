"""
(This question is a variation of the LeetCode question 295. Find Median from Data Stream. 
If you haven't completed that question yet, it is recommended to solve it first.)

In the world of big data, analysts often work with massive, unsorted datasets. 
Imagine you are given a very large and unsorted array of integers nums. 
Your task is to develop an efficient method to find its median.

The median is the middle value in an ordered dataset, which is defined as:

If the array contains an odd number of elements, the median is the single middle 
element after sorting. If the array contains an even number of elements, the median 
is the average of the two middle elements after sorting. Since the array can be 
extremely large, your solution must run in the time complexity of amortized 
O(N)

Constraints:
1 ≤ nums.length ≤ 10^5
-2^31 <= nums[i] < 2^31 - 1
"""
from collections import defaultdict
import heapq
class Solution:
    def __init__(self):
        self.left = []
        self.right = []
    
    # move max value in left to right
    def L2R(self):
        t = heapq.heappop(self.left)
        heapq.heappush(self.right, -t)

    # move min value in right to left
    def R2L(self):
        t = heapq.heappop(self.right)
        heapq.heappush(self.left, -t)

    def findMedian(self, nums):
        # principle: left num 
        # for each num, put into left first
        # then pop out the max num from left, move it into right
        for num in nums:
            heapq.heappush(self.left, -num)

            t = heapq.heappop(self.left)
            heapq.heappush(self.right, -t)

            if len(self.right) > len(self.left) + 1:
                self.R2L()
        
        if len(self.right) == len(self.left) + 1:
            return float(self.right[0])
        else:
            return (self.right[0] - self.left[0]) / 2


def runTests():
    # 1) Single element
    s = Solution()
    assert s.findMedian([5]) == 5

    # 2) Odd count, unsorted
    s = Solution()
    assert s.findMedian([3, 1, 2]) == 2

    # 3) Even count, unsorted
    s = Solution()
    assert s.findMedian([4, 1, 2, 3]) == 2.5  # sorted: [1,2,3,4]

    # 4) With duplicates
    s = Solution()
    assert s.findMedian([2, 2, 2, 2]) == 2.0

    # 5) Negative numbers
    s = Solution()
    assert s.findMedian([-5, -1, -3]) == -3  # sorted: [-5,-3,-1]

    # 6) Mix negative and positive, even count
    s = Solution()
    assert s.findMedian([-1, 0, 1, 2]) == 0.5  # sorted: [-1,0,1,2]

    # 7) Large extremes (32-bit bounds style)
    s = Solution()
    assert s.findMedian([-(2**31), 2**31 - 1]) == (-1) / 2  # -0.5

    # 8) Already sorted increasing
    s = Solution()
    assert s.findMedian([1, 2, 3, 4, 5]) == 3

    # 9) Sorted decreasing
    s = Solution()
    assert s.findMedian([5, 4, 3, 2, 1]) == 3

    # 10) Random-ish
    s = Solution()
    assert s.findMedian([10, 7, 2, 3, 5]) == 5  # sorted: [2,3,5,7,10]

    print("All tests passed!")

runTests()


"""
Top 3 most common follow-ups for this median problem:

1 Turn it into a real data stream
Implement addNum(x) and findMedian() (LeetCode 295).
Expect: two heaps, addNum: O(log n), findMedian: O(1).

2 Sliding window median
“Return median for every window of size k” (LeetCode 480).
Expect: two heaps + lazy deletion hash map, O(n log k).

3 Can’t store all data / very large dataset
“Data doesn’t fit memory—how to get median?”
Exact: external-memory selection / multi-pass counting (if bounded range) / distributed selection.
Approx: quantile sketch (e.g., GK / t-digest).
"""

# follow-up 1 Data stream Median
class MedianFinder:
    def __init__(self):
        self.left = []
        self.right = []
    
    def addNum(self, num):
        if not self.right or num >= self.right[0]:
            heapq.heappush(self.right, num)
        else:
            heapq.heappush(self.left, -num)
        
        # rebalance so that right has same count as left, or 1 more
        if len(self.right) > len(self.left) + 1:
            heapq.heappush(self.left, -heapq.heappop(self.right))
        elif len(self.left) > len(self.right):
            heapq.heappush(self.right, -heapq.heappop(self.left))
    
    def findMedian(self):
        if not self.right and not self.left:
            return 0.0
        
        if len(self.right) == len(self.left) + 1:
            return float(self.right[0])
        
        return (self.right[0] - self.left[0]) / 2.0
    
def testMedianFinder():
    mf = MedianFinder()
    for x in [3, 1, 2]:
        mf.addNum(x)
    assert mf.findMedian() == 2.0

    mf = MedianFinder()
    for x in [4, 1, 2, 3]:
        mf.addNum(x)
    assert mf.findMedian() == 2.5

    mf = MedianFinder()
    for x in [-1, 0, 1, 2]:
        mf.addNum(x)
    assert mf.findMedian() == 0.5

testMedianFinder()

# sliding window median
# use lazyHeap
class DualHeap:
    def __init__(self, k):
        self.small = [] # max-heap for smaller part
        self.large = [] # min-heap for larger part
        self.delayed = defaultdict(int) # # record already deleted num
        self.smallSize = 0 # record real size for small
        self.largeSize = 0 # record real size for large
        self.k = k

    # clean deleted num on top
    def _pruneSmall(self):
        while self.small:
            num = -self.small[0]
            if self.delayed[num] > 0:
                heapq.heappop(self.small)
                self.delayed[num] -= 1
            else:
                break
    # clean deleted num on top
    def _pruneLarge(self):
        while self.large:
            num = self.large[0]
            if self.delayed[num] > 0:
                heapq.heappop(self.large)
                self.delayed[num] -= 1
            else:
                break
    # rebalance via compare smallSize and largeSize
    def _makeBalance(self):
        # keep smallSize == largeSize or smallSize == largeSize + 1
        if self.smallSize > self.largeSize + 1:
            val = -heapq.heappop(self.small)
            self.smallSize -= 1
            heapq.heappush(self.large, val)
            self.largeSize += 1
            self._pruneSmall() # prune the new top in small
        elif self.smallSize < self.largeSize:
            val = heapq.heappop(self.large)
            self.largeSize -= 1
            heapq.heappush(self.small, -val)
            self.smallSize += 1
            self._pruneLarge()

    # add new head to heap
    def add(self, num):
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
            self.smallSize += 1
        else:
            heapq.heappush(self.large, num)
            self.largeSize += 1
        self._makeBalance()
        
    # remove old tail of window from heap
    def remove(self, num):
        self.delayed[num] += 1

        if self.small and num <= -self.small[0]:
            self.smallSize -= 1
            if num == -self.small[0]:
                self._pruneSmall()
        else:
            self.largeSize -= 1
            if num == self.large[0]:
                self._pruneLarge()
        
        self._makeBalance()

    def getMedian(self):
        if self.k % 2 == 1:
            return float(-self.small[0])
        return (self.large[0] - self.small[0]) / 2.0


def medianSlidingWindow(nums, k):
    if k <= 0 or not nums or k > len(nums):
        return []
    
    dh = DualHeap(k)
    for i in range(k):
        dh.add(nums[i])
    
    res = [dh.getMedian()]

    for i in range(k, len(nums)):
        dh.add(nums[i])
        dh.remove(nums[i - k])
        res.append(dh.getMedian())
    
    return res
    

def testMedianSlidingWindow():
    assert medianSlidingWindow([1,3,-1,-3,5,3,6,7], 3) == [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
    assert medianSlidingWindow([1,2,3,4], 2) == [1.5, 2.5, 3.5]
    assert medianSlidingWindow([2,2,2,2], 2) == [2.0, 2.0, 2.0]

testMedianSlidingWindow()

"""
3) Too Large to Fit Memory (Exact) — Bounded Value Range
If values are within a known small range [minVal, maxVal], you can compute the median with counts.
Time: O(n + R) where R = maxVal - minVal + 1
Space: O(R) (no need to store all numbers)
"""
def medianFromIteratorBoundedRange(numsIter, minVal, maxVal):
    if minVal > maxVal:
        return 0.0
    
    size = maxVal - minVal + 1
    counts = [0] * size
    total = 0

    for x in numsIter:
        counts[x - minVal] += 1
        total += 1
    
    if total == 0:
        return 0.0
    
    k1 = (total - 1) // 2 # left num for median
    k2 = total // 2   # right num for median

    def findKth(k):
        running = 0
        for i, cnt in enumerate(counts):
            running += cnt
            if running > k:
                return i + minVal
        return maxVal # should never hit
    
    a = findKth(k1)
    b = findKth(k2)
    return (a + b) / 2.0
