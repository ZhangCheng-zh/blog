"""
Design a meeting room scheduler for a predefined set of meeting rooms identified by their unique room IDs (e.g., ["roomA", "roomB", ...]).
Implement the MeetingScheduler class:

MeetingScheduler(List<String> roomList) Initializes the scheduler system with the given list of room IDs.
String schedule(int start, int end) Schedule a meeting in one of the available rooms between the start and end time.

If multiple rooms are available, assign the room with the lexicographically smallest room ID.
If no rooms are available for the specified time slot, return an empty string.
"""
from bisect import bisect_left
class MeetingScheduler:
    def __init__(self, roomList):
        self.rooms = sorted(roomList)
        self.roomMeetings = { roomId: [] for roomId in self.rooms }
    
    def schedule(self, start, end):
        for roomId in self.rooms:
            meetings = self.roomMeetings[roomId]

            idx = bisect_left(meetings, (start, end))

            if idx > 0 and meetings[idx - 1][1] > start:
                continue

            if idx < len(meetings) and meetings[idx][0] < end:
                continue
                

            meetings.insert(idx, (start, end))
            return roomId
        return ''
    
def runTests():
    # Example 1
    scheduler = MeetingScheduler(["roomB", "roomA", "roomC"])
    assert scheduler.schedule(1, 5) == "roomA"
    assert scheduler.schedule(1, 5) == "roomB"
    assert scheduler.schedule(2, 6) == "roomC"
    assert scheduler.schedule(2, 3) == ""
    assert scheduler.schedule(5, 10) == "roomA"
    assert scheduler.schedule(8, 10) == "roomB"

    # Example 2
    scheduler = MeetingScheduler(["roomA"])
    assert scheduler.schedule(1, 5) == "roomA"
    assert scheduler.schedule(1, 5) == ""
    assert scheduler.schedule(5, 10) == "roomA"
    assert scheduler.schedule(2, 6) == ""

    # Example 3
    scheduler = MeetingScheduler(["roomA", "roomB"])
    assert scheduler.schedule(1, 3) == "roomA"
    assert scheduler.schedule(2, 4) == "roomB"
    assert scheduler.schedule(3, 5) == "roomA"
    assert scheduler.schedule(1, 2) == "roomB"   # fits before [2,4)
    assert scheduler.schedule(4, 6) == "roomB"   # fits after [2,4)
    assert scheduler.schedule(8, 10) == "roomA"

    print("All tests passed!")


runTests()
