"""
Sliding Window Averages Ignoring Top-k

You are given:
an integer array nums
an integer windowSize
an integer k

For every contiguous subarray (sliding window) of length windowSize, compute the average of the window after removing
(ignoring) the largest k values in that window.

Return a list ans where:
ans[i] is the average for the window nums[i : i + windowSize] after ignoring its largest k numbers.

Notes
“Ignore the largest k numbers” means: remove exactly k elements with the greatest values in the window 
(if there are duplicates, remove any k of them).
"""
from sortedcontainers import SortedList
# a window with s size
# use sortedDict to contain all num in window
# after each update 
def slidingWindowAvg(nums, windowSize, k):
    result = []
    if nums is None or len(nums) < windowSize or k < 0 or k >= windowSize:
        return result
    
    n = len(nums)
    
    window = SortedList(nums[:windowSize])
    windowSum = sum(nums[:windowSize])
    keepCnt = windowSize - k 

    def topKSum():
        s = 0
        for i in range(1, k + 1):
            s += window[-i]
        return s
    
    # init ans 
    ans = [(windowSum - topKSum()) / keepCnt]

    for r in range(windowSize, n):
        oldV = nums[r - windowSize]
        inV = nums[r]

        window.remove(oldV) # remove old num out
        window.add(inV)  # add new num into sortedlist
        windowSum += inV - oldV # update sum of window

        ans.append((windowSum - topKSum()) / keepCnt)
    # time O(n(logw + k)) space O(w)
    return ans

    