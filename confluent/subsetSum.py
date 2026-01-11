"""
nums = [a1, a2, ..., an]
target = T

Q1 if has a subset of nums which sum is target
Q2 return a valid subset
"""






from functools import cache

# time O(2^n) space O(n)
def subsetSum(nums, target):
    n = len(nums)
    # check if pick the idx num, and presum is temp sum
    def backtrack(idx, presum):
        if presum == target:
            return True
        # no more num can be picked or temp sum already larger than target
        if idx >= n or presum > target:
            return False
        
        # not pick num
        if backtrack(idx + 1, presum) or backtrack(idx + 1, presum + nums[idx]):
            return True
        
        return False

    return backtrack(0, 0)

# time: O(n * target) space O(target)
def subsetSumDP(nums, target):
    n = len(nums)
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        # why reverse iterate, because need smaller target dp
        for t in range(target, num - 1, -1):
            dp[t] = dp[t] or dp[t - num] # if not pick target num or pick target num
    
    return dp[target]

# time: O(n * target) space O(n * target)
def subsetSumDP2D(nums, target):
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True

    for i in range(n + 1):
        dp[i][0] = True

    for i in range(n):
        start = nums[i]
        for t in range(target + 1):
            dp[i + 1][t] = dp[i][t] or (t >= start and dp[i][t - start])
    
    return dp[-1][-1]


print(subsetSumDP2D([1,2,3,4], 3))
print(subsetSumDP2D([1,2,3,4], 10))
print(subsetSumDP2D([1,2,3,4], 12))
print(subsetSumDP2D([1,3,5], 2))

# time O(2^n) space O(n)
def subsetSumPath(nums, target):
    n = len(nums)

    def backtrack(idx, path):
        if sum(path) == target:
            return True,path[:]
        
        if idx >= n or sum(path) > target:
            return False, []
        
        # not pick nums[idx]
        valid, res = backtrack(idx + 1, path)
        if valid:
            return valid, res

        # pick nums[idx]
        path.append(nums[idx])

        valid, res = backtrack(idx + 1, path)
        if valid:
            return valid, res

        # restore
        path.pop()

        return False, []
    
    return backtrack(0, [])
    

# time: O(n * target) space O(n * target)
def subsetSumPathDP2D(nums, target):
    # dp[i][j] = -1 -> impossible using first i numbers to make sum j
    #             0 -> possible, and we did not pick nums[i - 1]
    #             1 -> possible, and we did pick nums[i - 1]
    n = len(nums)
    dp = [[-1] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = 0 # no num, target is 0, so no pick

    for i in range(n):
        num = nums[i]
        for j in range(target + 1):
            # not pick
            # without num, can still match sum j
            if dp[i][j] != -1:
                dp[i + 1][j] = 0

            # pick
            if j >= num and dp[i][j - num] != -1:
                dp[i + 1][j] = 1
    
    if dp[-1][-1] == -1:
        return False, []
    
    path = []
    i, j = n, target
    while i > 0 and j >= 0:
        choice = dp[i][j]
        if choice == 1:
            num = nums[i - 1]
            path.append(num)
            j -= num
        i -= 1
    
    path.reverse()
    return True, path

def subsetSumPathDP(nums, target):
    dp = [-1] * (target + 1)
    dp[0] = 1 # means target == 0 always has answer

    for i, num in enumerate(nums):
        for t in range(target, num - 1, -1):
            if dp[t] == -1 and dp[t - num] != -1:
                dp[t] = i
    
    if dp[target] == -1:
        return False, []
    
    res = []
    t = target
    while t > 0:
        res.append(nums[dp[t]])
        t -= nums[dp[t]]
    
    return True, res[::-1]

# def subsetSumPathDP(nums, target):
#     dp = [-1] * (target + 1)
#     dp[0] = -2

#     for i, num in enumerate(nums):
#         for t in range(target, num - 1, -1):
#             if dp[t] == -1 and dp[t - num] != -1:
#                 dp[t] = i # the latest num chose
    
#     if dp[target] == -1:
#         return False, []
    
#     res = []
#     t = target
#     while t > 0:
#         i = dp[t]
#         res.append(nums[i])
#         t -= nums[i]
#     return True, res[::-1]


print(subsetSumPathDP([1,2,3,4], 3))
print(subsetSumPathDP([1,2,3,4], 10))
print(subsetSumPathDP([1,2,3,4], 12))
print(subsetSumPathDP([1,3,5], 2))

# ---------- More tests for subset sum (exists + path) ----------

def assertExistsAll(nums, target, expected):
    assert subsetSum(nums, target) == expected
    assert subsetSumDP(nums, target) == expected
    assert subsetSumDP2D(nums, target) == expected

def assertPathAll(nums, target, expectedExists):
    ok1, path1 = subsetSumPath(nums, target)
    ok2, path2 = subsetSumPathDP2D(nums, target)
    ok3, path3 = subsetSumPathDP(nums, target)

    assert ok1 == expectedExists
    assert ok2 == expectedExists
    assert ok3 == expectedExists

    if expectedExists:
        assert sum(path1) == target
        assert sum(path2) == target
        assert sum(path3) == target
        # each picked element must come from nums (multiset check is complex; keep it simple)
        for x in path1: assert x in nums
        for x in path2: assert x in nums
        for x in path3: assert x in nums
    else:
        assert path1 == []
        assert path2 == []
        assert path3 == []

# 1) empty nums
assertExistsAll([], 0, True)
assertPathAll([], 0, True)      # empty subset
assertExistsAll([], 5, False)
assertPathAll([], 5, False)

# 2) target = 0 (should always be True: empty subset)
assertExistsAll([1, 2, 3], 0, True)
assertPathAll([1, 2, 3], 0, True)

# 3) single element
assertExistsAll([7], 7, True)
assertPathAll([7], 7, True)
assertExistsAll([7], 3, False)
assertPathAll([7], 3, False)

# 4) duplicates (0/1 subset sum still ok)
assertExistsAll([2, 2, 2], 4, True)
assertPathAll([2, 2, 2], 4, True)
assertExistsAll([2, 2, 2], 6, True)
assertPathAll([2, 2, 2], 6, True)
assertExistsAll([2, 2, 2], 1, False)
assertPathAll([2, 2, 2], 1, False)

# 5) includes zero
assertExistsAll([0, 0, 5], 5, True)
assertPathAll([0, 0, 5], 5, True)
assertExistsAll([0, 0, 0], 0, True)
assertPathAll([0, 0, 0], 0, True)

# 6) multiple solutions exist (any one is acceptable)
assertExistsAll([1, 2, 3, 4, 5], 9, True)   # 4+5 or 2+3+4 etc.
assertPathAll([1, 2, 3, 4, 5], 9, True)

# 7) larger target near sum(nums)
assertExistsAll([3, 4, 6, 10], 23, True)    # all
assertPathAll([3, 4, 6, 10], 23, True)
assertExistsAll([3, 4, 6, 10], 24, False)
assertPathAll([3, 4, 6, 10], 24, False)

# 8) “tight” target that needs skipping big numbers
assertExistsAll([8, 1, 2, 9], 3, True)      # 1+2
assertPathAll([8, 1, 2, 9], 3, True)

# 9) classic subset-sum set
nums = [3, 34, 4, 12, 5, 2]
assertExistsAll(nums, 9, True)             # 4+5 or 3+4+2
assertPathAll(nums, 9, True)
assertExistsAll(nums, 30, False)
assertPathAll(nums, 30, False)

# 10) stress-ish small: many 1s
nums = [1] * 20
assertExistsAll(nums, 20, True)
assertPathAll(nums, 20, True)
assertExistsAll(nums, 21, False)
assertPathAll(nums, 21, False)
