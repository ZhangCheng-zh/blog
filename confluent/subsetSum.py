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

print(subsetSum([1,2,3,4], 3))
print(subsetSum([1,2,3,4], 10))
print(subsetSum([1,2,3,4], 12))
print(subsetSum([1,3,5], 2))

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


print(subsetSumDP([1,2,3,4], 3))
print(subsetSumDP([1,2,3,4], 10))
print(subsetSumDP([1,2,3,4], 12))
print(subsetSumDP([1,3,5], 2))

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
    

print(subsetSumPath([1,2,3,4], 3))
print(subsetSumPath([1,2,3,4], 10))
print(subsetSumPath([1,2,3,4], 12))
print(subsetSumPath([1,3,5], 2))


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


print(subsetSumPathDP2D([1,2,3,4], 3))
print(subsetSumPathDP2D([1,2,3,4], 10))
print(subsetSumPathDP2D([1,2,3,4], 12))
print(subsetSumPathDP2D([1,3,5], 2))

def subsetSumPathDP(nums, target):
    dp = [-1] * (target + 1)
    dp[0] = -2

    for i, num in enumerate(nums):
        for t in range(target, num - 1, -1):
            if dp[t] == -1 and dp[t - num] != -1:
                dp[t] = i # the latest num chose
    
    if dp[target] == -1:
        return False, []
    
    res = []
    t = target
    while t > 0:
        i = dp[t]
        res.append(nums[i])
        t -= nums[i]
    return True, res[::-1]


print(subsetSumPathDP([1,2,3,4], 3))
print(subsetSumPathDP([1,2,3,4], 10))
print(subsetSumPathDP([1,2,3,4], 12))
print(subsetSumPathDP([1,3,5], 2))