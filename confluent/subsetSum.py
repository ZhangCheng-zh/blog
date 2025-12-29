"""
nums = [a1, a2, ..., an]
target = T

Q1 if has a subset of nums which sum is target
Q2 return a valid subset
"""



from functools import cache


def subsetSum(nums, target):
    n = len(nums)
    ans = []
    path = []
    @cache
    def dfs(i, left): # start from ith number in nums, pick num make the sum is left
        
        # print('dfs', i, left)
        if left == 0: # has a subset of nums which sum is target
            nonlocal ans
            ans = path.copy()
            return True

        if left < 0:
            return False 
        
        if i == n: # all num already be picked, still cant match target
            return False 
        
        # not pick
        if dfs(i + 1, left):
            return True

        # pick the ith num
        path.append(nums[i])
        if dfs(i + 1, left - nums[i]):
            return True
        path.pop()
        
    hasAns = dfs(0, target) 

    return ans if hasAns else []
    

print(subsetSum([1,2,3,4], 3))
print(subsetSum([1,2,3,4], 10))
print(subsetSum([1,2,3,4], 12))
print(subsetSum([1,3,5], 2))


def subsetSumDP(nums, target):
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for t in range(target, num - 1, -1):
            dp[t] = dp[t] or dp[t - num]
    return dp[target]

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


    

print(subsetSumDP([1,2,3,4], 3))
print(subsetSumDP([1,2,3,4], 10))
print(subsetSumDP([1,2,3,4], 12))
print(subsetSumDP([1,3,5], 2))



print(subsetSumPathDP([1,2,3,4], 3))
print(subsetSumPathDP([1,2,3,4], 10))
print(subsetSumPathDP([1,2,3,4], 12))
print(subsetSumPathDP([1,3,5], 2))