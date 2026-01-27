"""
### Unbounded Matrix Connectivity

You have an **infinite 2D grid**. Some coordinates contain a **point**, others are empty.
You need to design a class that supports adding points and querying reachability between points.

A **move** from point `A` to point `B` is valid if:
* `A` and `B` are in the **same row** (`rowA == rowB`) **or** the **same column** (`colA == colB`)
* and **both coordinates already contain points**
* Each valid move costs **1 step**

Implement:
* `addPoint(row, col)`
  Add a point at `(row, col)`.
* `isConnected(point1, point2) -> bool`
  Return `True` if there exists a sequence of valid moves from `point1` to `point2`, otherwise `False`.
* `getMinSteps(start, end) -> int`
  Return the **minimum number of steps** to reach `end` from `start`. If impossible, return `-1`.

Notes:
* Coordinates are integers.
* The grid is unbounded.
* Each coordinate pair is unique (no duplicates).
* If either endpoint does not exist as a point, treat it as unreachable.

Example:
Points added: `(0,2)`, `(1,2)`, `(1,4)`
* `isConnected((0,2),(1,4)) = True` via `(1,2)`
* `getMinSteps((0,2),(1,4)) = 2` (`(0,2)->(1,2)->(1,4)`)
"""

from typing import List, Optional
from collections import defaultdict

class UnboundMatrix:
    def __init__(self):
        self.rowDict = defaultdict(list)
        self.colDict = defaultdict(list)

    def addPoint(self, x, y):
        self.rowDict[x].append(y)
        self.colDict[y].append(x)

    def isConnected(self, point1, point2):
        

    def getMinSteps(self, start, end):
        pass