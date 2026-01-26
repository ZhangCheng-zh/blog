"""
You are given a list of closed intervals on the number line, where each interval 
is represented as a pair [start, end] and includes both endpoints. Two intervals overlap 
at a point if that point lies in both intervals.

Determine the maximum number of intervals that overlap at any single point on 
the number line.

Constraints
1 <= intervals.length <= 10^5
-10^9 <= intervals[i][0] <= intervals[i][1] <= 10^9
"""
def maxOverLap(intervals):
    pipeline = []
    for s, e in intervals:
        pipeline.append((s, 1))
        pipeline.append((e + 1, -1))
    
    res = 0

    pipeline.sort()

    cnt = 0
    for x in pipeline:
        cnt += x[1]
        if cnt > res:
            res = cnt
    return res