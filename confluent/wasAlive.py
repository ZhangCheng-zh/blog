"""
Given timestamps for a key, determine whether within a sliding 500ms window starting at `start`, 
divided into 5 fixed 100ms buckets, the key appears in **at least 3 consecutive buckets**.
It is essentially a **time-bucket / sliding-window continuity detection** problem.
"""
from bisect import bisect_left
def wasAlive(records, key, start):
    buckets = [False] * 5
    for k, t in records:
        if k != key:
            continue
        if start <= t <= start + 499:
            idx = (t - start) // 100
            buckets[idx] = True
    for i in range(3):
        if all(buckets[i: i + 3]):
            return True
    return False


# Basic: 3 consecutive buckets (0,1,2) => True
records = [("a", 0), ("a", 101), ("a", 250)]
assert wasAlive(records, "a", 0) is True  # buckets: [T,T,T,F,F]

# Non-consecutive (0,2,4) => False
records = [("a", 0), ("a", 250), ("a", 450)]
assert wasAlive(records, "a", 0) is False  # [T,F,T,F,T]

# Exactly 3 consecutive buckets (2,3,4) => True
records = [("a", 200), ("a", 320), ("a", 499)]
assert wasAlive(records, "a", 0) is True  # [F,F,T,T,T]

# Boundary: include start and start+499, exclude start+500
records = [("a", 0), ("a", 99), ("a", 100), ("a", 199), ("a", 200)]
assert wasAlive(records, "a", 0) is True  # [T,T,T,F,F]
records = [("a", 500), ("a", 600), ("a", 700)]
assert wasAlive(records, "a", 0) is False  # all out of window

# Multiple events in same bucket still counts as one bucket => True
records = [("a", 10), ("a", 20), ("a", 110), ("a", 115), ("a", 210)]
assert wasAlive(records, "a", 0) is True  # [T,T,T,F,F]

# Wrong key ignored => False
records = [("b", 0), ("b", 120), ("b", 240), ("b", 360)]
assert wasAlive(records, "a", 0) is False

# Start offset: window [1000..1499], buckets 0..4 => True (0,1,2)
records = [("a", 1000), ("a", 1100), ("a", 1299)]
assert wasAlive(records, "a", 1000) is True  # [T,T,T,F,F]

# Start offset: consecutive buckets (1,2,3) => True
records = [("a", 1100), ("a", 1250), ("a", 1350)]
assert wasAlive(records, "a", 1000) is True  # [F,T,T,T,F]

# Only 2 consecutive buckets => False
records = [("a", 0), ("a", 150), ("a", 399)]
assert wasAlive(records, "a", 0) is False  # [T,T,F,T,F]

# Empty records => False
records = []
assert wasAlive(records, "a", 0) is False


def wasAliveFast(records, key, start, bucketSize = 100, bucketCount = 5, needConsecutive = 3):
    tw = [t for k, t in records if k == key]
    tw.sort()

    buckets = [False] * bucketCount
    for i in range(bucketCount):
        left = start + i * bucketSize
        right = left + bucketSize - 1
        idx = bisect_left(tw, left)
        # if has record in target bucket of tw, heartbeat true
        buckets[i] = (idx < len(tw) and tw[idx] <= right)
    

    run = 0
    for b in buckets:
        if b:
            run += 1
        else:
            run = 0
        if run >= needConsecutive:
            return True
    return False

# 11) custom params: need 4 consecutive buckets
records = [("a", 0), ("a", 100), ("a", 200), ("a", 300)]
assert wasAliveFast(records, "a", 0, needConsecutive=4) is True
records = [("a", 0), ("a", 100), ("a", 200)]
assert wasAliveFast(records, "a", 0, needConsecutive=4) is False

# 12) custom params: bucketSize=50ms, 10 buckets, need 3 consecutive
records = [("a", 0), ("a", 60), ("a", 120)]  # buckets 0,1,2 with size 50
assert wasAliveFast(records, "a", 0, bucketSize=50, bucketCount=10, needConsecutive=3) is True