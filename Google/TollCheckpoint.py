"""
Toll Checkpoint Billing
A highway has multiple toll checkpoints. Each time a vehicle passes a checkpoint, 
the system records a log entry containing:
license plate
checkpoint name
timestamp

The checkpoint name is an alphanumeric string like "A1", "C7", "D10".
Its numeric part represents the checkpoint position on the highway.

Toll fee rule
The toll fee for traveling between two checkpoints is calculated by taking the absolute difference 
between their positions and multiplying it by 10 (excluding any characters). 
For example, the toll fee for a vehicle passing through checkpoints "A1" and "A5" is calculated as |1 - 5| * 10 = 40.
"""
from collections import defaultdict

def getTrailingNumber(s):
    i = len(s) - 1
    while i >= 0 and s[i].isdigit():
        i -= 1
    return int(s[i + 1:])

def calculateFee(logEntries):
    carLog = defaultdict(list)
    logs = [item.split(',') for item in logEntries]
    for car, position, timestamp in logs:
        p = getTrailingNumber(position)
        carLog[car].append([int(timestamp), p])
    
    fees = defaultdict(int)

    for k, vs in carLog.items():
        vs.sort()
        startTime, startP = vs[0]
        for t, p in vs[1:]:
            if t > startTime:
                fees[k] += abs(p - startP) * 10
            startTime = t 
            startP = p

    return [f'License: {k}, Fee: {v}' for k, v in fees.items()]



def runTests():
    tests = [
        # Example 1
        (
            ["CAR123,A1,1000", "CAR123,A5,2000"],
            ["License: CAR123, Fee: 40"],
        ),

        # Example 2 (order of results can vary, so we compare as sets)
        (
            ["CAR111,C2,1100", "CAR111,C4,1300",
             "CAR222,C1,1000", "CAR222,C3,1500", "CAR222,C7,2000"],
            ["License: CAR111, Fee: 20", "License: CAR222, Fee: 60"],
        ),

        # Example 3
        (
            ["CAR999,D10,3000", "CAR999,D1,1000", "CAR999,D5,2000"],
            ["License: CAR999, Fee: 90"],
        ),

        # Interleaved multi-cars, out-of-order logs
        (
            ["A,A4,1500", "B,B2,1200", "A,A1,1000", "B,B5,1000", "B,B9,2000"],
            ["License: A, Fee: 30", "License: B, Fee: 100"],
        ),

        # Repeated checkpoint => 0 segment
        (
            ["CAR1,A3,1000", "CAR1,A3,2000", "CAR1,A8,3000"],
            ["License: CAR1, Fee: 50"],
        ),

        # Same timestamp (your code ignores hops where t == startTime)
        (
            ["T1,X1,1000", "T1,X10,1000", "T1,X5,2000"],
            ["License: T1, Fee: 50"],
        ),

        # Multi-digit positions
        (
            ["CAR2,Z10,1000", "CAR2,Z2,2000", "CAR2,Z15,3000"],
            ["License: CAR2, Fee: 210"],
        ),
    ]

    for i, (logs, expected) in enumerate(tests, 1):
        got = calculateFee(logs)
        assert set(got) == set(expected), f"Test {i} failed.\nExpected: {expected}\nGot: {got}"

    print("All tests passed!")


if __name__ == "__main__":
    runTests()