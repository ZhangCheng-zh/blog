"""
You are given a list of order deliveries scheduled for the day including start time, end time, d
nd dollar amount for completing each order delivery. Assuming only one order can be delivered 
at a time, determine the maximum amount of money that can made from the given deliveries. 
Note: deliveries cannot happen outside the given time constraints for the day

The inputs are as follows: 
start_time = 0 // deliveries for the day cannot start before this time
end_time = 10  // deliveries for the day can’t end after this time
// start time, end time and pay for each order delivery
d_starts = [2, 3, 5, 7] /
d_ends = [6, 5, 10, 11] 
d_pays = [5, 2, 4, 1] 

The output should be an integer representing the maximum amount of money made from deliveries. 
Expected output: 6

# [2, 6, 5] [3, 5, 2] [5, 10, 4] [7, 11, 1]
"""

from bisect import bisect_left

def maxDeliveryPay(starts, ends, pays):
    n = len(starts)
    items = [(s, e, p) for s, e, p in zip(starts, ends, pays)]

    items.sort(key = lambda x: x[1])
    ends.sort()

    # dp[i] mean consider pre ith deliverys, the max pay can get
    # dp[0] = 0 means no pay get with no delivery
    dp = [0] * (n + 1)

    for i in range(n):
        s, e, p = items[i]

        # skip this delivery
        skip = dp[i]

        # pick this delivery
        # find last delivery which is valid, search on [0, i)
        lastValidIdx = bisect_left(ends, s, 0, i)
        # all end in ends[:lastValidIdx] is smaller than s

        take = dp[lastValidIdx] + p

        dp[i + 1] = max(skip, take)
    return dp[-1]


# 0) Empty
assert maxDeliveryPay([], [], []) == 0

# 1) Touching boundary NOT allowed: end == start is invalid
# Can't do (1,3) then (3,5)
assert maxDeliveryPay([1, 3], [3, 5], [5, 6]) == 6

# 2) Gap is allowed: end < start
assert maxDeliveryPay([1, 4], [3, 6], [5, 6]) == 11  # (1,3,5) + (4,6,6)

# 3) Prompt-like example but STRICT rule:
# (3,5) + (5,10) is NOT allowed, so best is (2,6,5) = 5
assert maxDeliveryPay([2, 3, 5], [6, 5, 10], [5, 2, 4]) == 5

# 4) Multiple non-overlapping with gaps
assert maxDeliveryPay([1, 3, 5], [2, 4, 6], [3, 4, 5]) == 12  # 3+4+5

# 5) Nested vs many small: choose many small ones
# (2,3,3)+(4,5,4)+(6,7,5)+(8,9,6) = 18 beats (1,10,10)
assert maxDeliveryPay([1, 2, 4, 6, 8], [10, 3, 5, 7, 9], [10, 3, 4, 5, 6]) == 18

# 6) Overlaps + strict boundary prevents chaining at equality
# (1,4) cannot chain with (4,7)
assert maxDeliveryPay([1, 2, 4], [4, 6, 7], [5, 6, 5]) == 6

# 7) Big profit job + later job with a gap
# (2,4,100) + (6,7,10) = 110
assert maxDeliveryPay([1, 2, 3, 6], [2, 4, 5, 7], [5, 100, 7, 10]) == 110

# 8) Same end times, and a touching-start job (should NOT chain)
# Best is just (3,5,7)
assert maxDeliveryPay([1, 2, 3], [3, 3, 5], [5, 6, 7]) == 7

# 9) Zero/negative pay should be avoidable
assert maxDeliveryPay([1, 3, 5], [2, 4, 6], [0, -5, 10]) == 10

print("✅ All tests passed!")
