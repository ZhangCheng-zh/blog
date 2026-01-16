"""
Given a list of log events represented as a 2D string array logs, where each log entry contains three elements: task_name, 
an action ("enter" or "exit"), and a timestamp:
"enter" indicates the start of a task.
"exit" indicates the completion of a task.
Calculate the total time the CPU spends executing each task. 
Return the results as a list of strings in the format "task_name: total_time", sorted alphabetically by task names.

Note that the CPU is single-threaded, meaning it can only process one task at a time. Tasks may overlap, and when the CPU completes a task, if multiple tasks are waiting, it always resumes the most recently added task.
"""
from collections import defaultdict
class Solution:
    def cpuTimeByTask(self, logs):
        logs.sort(key = lambda x: int(x[2])) # sort by timestamp first

        timeByTask = defaultdict(int) # total cpu time spent running this task
        stack = [] # call stack of currently active tasks

        # prevTime is timestamp of the last processed log event
        # the time interval (prevTime -> currentTime) belongs to stack[-1]
        prevTime = None 

        for task, action, tsStr in logs:
            ts = int(tsStr)

            if prevTime is None:
                prevTime = ts
            
            # time since prevTime belongs to current running task 
            if stack:
                timeByTask[stack[-1]] += ts - prevTime

            # now handle the current event at time ts:
            if action == 'enter':
                stack.append(task)
            else:
                stack.pop()
            
            # more prevTime forward to current timestamp for the next interval
            prevTime = ts
        
        return [f'{name}: {timeByTask[name]}' for name in sorted(timeByTask)]


def runTests():
    sol = Solution()

    logs1 = [
        ["print", "enter", "10"],
        ["malloc", "enter", "12"],
        ["malloc", "exit", "14"],
        ["write", "enter", "16"],
        ["write", "exit", "18"],
        ["write", "enter", "20"],
        ["write", "exit", "22"],
        ["print", "exit", "24"],
    ]
    assert sol.cpuTimeByTask(logs1) == ["malloc: 2", "print: 8", "write: 4"]

    logs2 = [
        ["task1", "enter", "0"],
        ["task3", "exit", "6"],
        ["task2", "exit", "8"],
        ["task2", "enter", "2"],
        ["task3", "enter", "4"],
        ["task1", "exit", "10"],
    ]
    assert sol.cpuTimeByTask(logs2) == ["task1: 4", "task2: 4", "task3: 2"]

    logs3 = [
        ["taskA", "enter", "0"],
        ["taskA", "exit", "5"],
        ["taskA", "enter", "6"],
        ["taskA", "exit", "10"],
        ["taskB", "enter", "10"],
        ["taskB", "exit", "15"],
    ]
    assert sol.cpuTimeByTask(logs3) == ["taskA: 9", "taskB: 5"]

    print("All tests passed!")


runTests()
