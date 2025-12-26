"""
Problem: Thread-Safe Time-Based Key-Value Store with Windowed Average

Design and implement a high-throughput time-based key-value store that supports storing multiple values for the same key at different timestamps and querying values at a given time.

In addition to standard time-based lookup, the store must support computing a sliding-window average over recent numeric values, where values older than the window are considered expired for the average calculation.

Because the system is used in a concurrent environment, your implementation must be thread-safe.

Implement TimeMap
Constructor

TimeMap(): Initializes the data structure.

Methods
set(key: str, value: str, timestamp: int) -> None

Stores the value for the given key at the given timestamp.

Notes:

A key may be stored many times at different timestamps.

You may assume that for the same key, timestamps provided to set are non-decreasing.

get(key: str, timestamp: int) -> str

Returns the value such that:

It was previously stored using set(key, value, timestamp_prev)

timestamp_prev <= timestamp

and timestamp_prev is the largest such timestamp

If no such value exists, return "".

getAverage(key: str, timestamp: int, window: int) -> float

Computes the average of numeric values for a key within a sliding window ending at timestamp.

Only values with timestamps in:

[timestamp - window + 1, timestamp]
are included. Values outside this range are considered expired for the purpose of the average.

Rules:

If a stored value is not numeric (cannot be parsed as a float), it is ignored for average computation.

If there are no numeric values in the window, return 0.0.

Concurrency Requirement

Your solution must be thread-safe and should allow high throughput by minimizing contention:

Operations on different keys should proceed concurrently when possible.

You may use a global lock only for managing shared metadata (like per-key structures), and a per-key lock for updating/querying data for that key.

Example
tm = TimeMap()
tm.set("foo", "10", 1)
tm.set("foo", "20", 3)
tm.set("foo", "bar", 4)

tm.get("foo", 2)            # "10"
tm.get("foo", 4)            # "bar"

tm.getAverage("foo", 4, 4)  # window [1..4] -> numeric values: 10, 20 -> avg = 15.0
tm.getAverage("foo", 4, 2)  # window [3..4] -> numeric values: 20 -> avg = 20.0
tm.getAverage("foo", 2, 1)  # window [2..2] -> none -> 0.0

Complexity Targets

set: amortized O(1)

get: O(log n) for that key

getAverage: O(log n) for that key

Thread-safe with minimal contention
"""

from bisect import bisect_left, bisect_right
import threading
from typing import Dict, List

class TimeMap:
    def __init__(self):
        # key -> (times, vals)
        self.times: Dict[str, List[int]] = {}
        self.vals: Dict[str, List[str]] = {}

        # key -> (num_times, prefix_sum) where prefix_sum[0] = [0.0]
        self.numTimes: Dict[str, List[int]] = {}
        self.numPrefix: Dict[str, List[float]] = {}

        # per-key locks + a meta lock to safely create them
        self.locks: Dict[str, threading.Lock] = {}
        self.metaLock = threading.Lock()
    
    def set(self, key, value, timestamp) -> None:
        # create/fetch lock and per-key containers safely
        with self.metaLock:
            lock = self.locks.get(key)
            if lock is None:
                lock = threading.Lock()
                self.locks[key] = lock
            
            if key not in self.times:
                self.times[key] = []
                self.vals[key] = []
                self.numTimes[key] = []
                self.numPrefix[key] = [0.0] # prefix sums
            
            times = self.times[key]
            vals = self.vals[key]
            numTimes = self.numTimes[key]
            numPrefix = self.numPrefix[key]
        
        with lock:
            times.append(timestamp)
            vals.append(value)
            # numeric track for getAverage
            try:
                num = float(value)
            except ValueError:
                return 
            numTimes.append(timestamp)
            numPrefix.append(numPrefix[-1] + num)
    
    def get(self, key: str, timestamp: int) -> str:
        with self.metaLock:
            lock = self.locks.get(key)
            times = self.times.get(key)
            vals = self.vals.get(key)

        if lock is None or not times:
            return ''
        
        with lock:
            i = bisect_right(times, timestamp) - 1
            return '' if i < 0 else vals[i]
    
    def getAverage(self, key, timestamp, window) -> float:
        if window <= 0:
            return 0.0

        left_ts = timestamp - window + 1

        with self.metaLock:
            lock = self.locks.get(key)
            times = self.numTimes.get(key)
            prefix = self.numPrefix.get(key)
        if lock is None or not times:
            return 0.0

        with lock:
            l = bisect_left(times, left_ts)
            r = bisect_right(times, timestamp)

            total = prefix[r] - prefix[l]
            return total / (r - l)

        