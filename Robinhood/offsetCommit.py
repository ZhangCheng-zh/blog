"""
## Offset Commit Ordering
You process messages from a stream.
Each message has a unique integer **offset** starting from **0**.

Messages may be **processed out of order** (multi-threaded), but a **commit** must always be **contiguous from 0**:
* Committing offset `x` means offsets `0..x` are all done.
* After processing each offset, if you have a continuous completed block `0..k`, you must commit **the largest such `k`**.
* If offset `0` is not yet processed (or the block is broken), you cannot commit anything and output `-1`.

### Task
Given an array `offsets` in the order they are processed, return an array `res` of the same length:
* `res[i] = k` if after processing `offsets[i]` you can commit up to `k` (the largest contiguous block from 0)
* otherwise `res[i] = -1`

### Example
Input: `offsets = [2, 0, 1]`
Output: `[-1, 0, 2]`
"""

def commitOffsets(offsets):
    seen = set()
    nextCommit = 0
    res = []

    for x in offsets:
        seen.add(x)

        before = nextCommit
        while nextCommit in seen:
            nextCommit += 1
        
        if nextCommit > before:
            res.append(nextCommit - 1)
        else:
            res.append(-1)
    return res

# T1: example 1
offsets = [2, 0, 1]
expected = [-1, 0, 2]
assert commitOffsets(offsets) == expected

# T2: example 2
offsets = [0, 1, 2]
expected = [0, 1, 2]
assert commitOffsets(offsets) == expected

# T3: example 3
offsets = [2, 1, 0, 5, 4]
expected = [-1, -1, 2, -1, -1]
assert commitOffsets(offsets) == expected

# T4: single offset 0
offsets = [0]
expected = [0]
assert commitOffsets(offsets) == expected

# T5: start missing for a while
offsets = [3, 2, 1, 0]
expected = [-1, -1, -1, 3]
assert commitOffsets(offsets) == expected

# T6: gaps remain unfilled
offsets = [0, 2, 4, 1]
expected = [0, -1, -1, 2]
assert commitOffsets(offsets) == expected

# T7: larger jump after filling gaps
offsets = [5, 0, 1, 4, 2, 3]
expected = [-1, 0, 1, -1, 2, 5]
assert commitOffsets(offsets) == expected
