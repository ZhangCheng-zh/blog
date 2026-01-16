"""
Candlestick Aggregation (10-unit intervals)
You receive price updates for one stock as (time, price) pairs. Times are non-negative integers. The pairs may be in any order.
For every 10 time units, build candlestick data for each interval:
Interval start time: t0 = (time // 10) * 10 (bucket [t0, t0+10))

For each interval output:
[t0, maxPrice, minPrice, openPrice, closePrice]
openPrice: price at the earliest time in that interval
closePrice: price at the latest time in that interval
maxPrice: highest price in that interval
minPrice: lowest price in that interval

Missing intervals (gap filling)
If an interval has no prices, but there was a previous interval output, then fill the missing interval
using the previous interval’s closePrice for all fields:
[t0, prevClose, prevClose, prevClose, prevClose]
If there is no previous interval yet (no earlier data), skip leading empty intervals.

Output
Return the candlesticks in increasing order of t0.
"""

from collections import defaultdict
def buildCandles(timePrices):
    if not timePrices:
        return []
    
    buckets = defaultdict(list)
    for t, p in timePrices:
        start = (t // 10) * 10
        buckets[start].append((t, p))
    
    starts = sorted(buckets.keys())
    res = []

    prevClose = None
    curStart = starts[0]

    while True:
        if curStart in buckets:
            ps = buckets[curStart]
            ps.sort()

            openPrice = ps[0][1]
            clostPrice = ps[-1][1]
            maxPrice = max(p for _, p in ps)
            minPrice = min(p for _, p in ps)
            res.append([curStart, maxPrice, minPrice, openPrice, clostPrice])
            prevClose = clostPrice
        else:
            res.append([curStart, prevClose, prevClose, prevClose, prevClose])
        
        if curStart == starts[-1]:
            break

        curStart += 10
    # time O(nlgn) n is length of timePrices
    return res



# T1: given example (unsorted input, with gaps to fill)
timePrices = [[1, 2], [3, 4], [9, 8], [5, 10], [13, 18], [34, 32], [55, 44]]
expected = [
    [0, 10, 2, 2, 8],
    [10, 18, 18, 18, 18],
    [20, 18, 18, 18, 18],
    [30, 32, 32, 32, 32],
    [40, 32, 32, 32, 32],
    [50, 44, 44, 44, 44],
]
assert buildCandles(timePrices) == expected

# T2: two intervals, no gaps
timePrices = [[0, 5], [3, 6], [9, 7], [10, 10], [11, 9], [15, 12], [19, 5]]
expected = [
    [0, 7, 5, 5, 7],
    [10, 12, 5, 10, 5],
]
assert buildCandles(timePrices) == expected

# T3: single point
timePrices = [[0, 10]]
expected = [[0, 10, 10, 10, 10]]
assert buildCandles(timePrices) == expected

# T4: open/close from earliest/latest time in the same bucket (input unsorted)
timePrices = [[8, 100], [1, 50], [9, 70], [2, 60]]
expected = [[0, 100, 50, 50, 70]]
assert buildCandles(timePrices) == expected

# T5: leading empty buckets are skipped (first bucket is 20)
timePrices = [[25, 10]]
expected = [[20, 10, 10, 10, 10]]
assert buildCandles(timePrices) == expected

# T6: multiple missing buckets filled with previous close
timePrices = [[1, 5], [41, 7]]
expected = [
    [0, 5, 5, 5, 5],
    [10, 5, 5, 5, 5],
    [20, 5, 5, 5, 5],
    [30, 5, 5, 5, 5],
    [40, 7, 7, 7, 7],
]
assert buildCandles(timePrices) == expected

# T7: boundary between buckets (9 in bucket 0, 10 in bucket 10)
timePrices = [[9, 1], [10, 2]]
expected = [
    [0, 1, 1, 1, 1],
    [10, 2, 2, 2, 2],
]
assert buildCandles(timePrices) == expected

print("All tests passed!")
