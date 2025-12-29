"""
Given timestamps for a key, determine whether within a sliding 500ms window starting at `start`, 
divided into 5 fixed 100ms buckets, the key appears in **at least 3 consecutive buckets**.
It is essentially a **time-bucket / sliding-window continuity detection** problem.
"""

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