"""
You are given a string s consisting of alphabetic characters ('A'-'Z', 'a'-'z). Build a binary tree that represents the frequency distribution of characters in s under the following conditions:

Leaf Nodes:
Each distinct character in s must appear exactly once as a leaf node.
A leaf node contains:
ch: the character itself.
count: the number of times that character appears in s.
Internal Nodes:
Every internal node must have:
ch set to '#'.
count equal to the sum of the count values of all leaves in its subtree.
Tree Construction Rules:
The tree must be built such that less frequent characters are combined earlier, and more frequent characters appear closer to the root.
If two characters have the same frequency, the one with the smaller lexicographic value is considered less frequent and must be combined earlier.
The first internal node is formed by combining the two characters with the lowest frequency, with the lower one placed on the left and the higher one on the right.
Every subsequent internal node is formed by combining:
The next character (based on frequency and tie-break rules) as the left child.
The previously constructed subtree as the right child.
You are provided with the following class definition:

class TreeNode {
    char ch;
    int count;
    TreeNode left;
    TreeNode right;
}
Return this node as the root of the tree.

Constraints:

1 ≤ s.length ≤ 10⁴
s consists only of uppercase and lowercase English letters.
Example 1:

Input: s = "aabbbbbcDDD"
Output: ["#, 11", "b, 5", "#, 6",  "D, 3", "#, 3", "c, 1", "a, 2"]
Explanation: The string has four distinct characters with frequencies: {'a': 2, 'b': 5, 'c': 1, 'D': 3}. These are merged step by step, always combining the two nodes with the smallest counts, until one root remains with a count 11.
The tree can be visualized as follows:


Example 2:

Input: s = "AABBC"
Output: [ "#, 5", "B, 2", "#, 3", "C, 1", "A, 2"]

Example 3:

Input: s = "AAAaaaBBBbbb"
Output: ["#, 12", "b, 3", "#, 9", "a, 3", "#, 6", "A, 3", "B, 3"]
"""

"""
Design a queue data structure that, in addition to the standard enqueue and dequeue operations, supports retrieving the minimum and maximum elements currently in the queue. All operations must be performed in O(1).

Implement the MinMaxQueue class:

MinMaxQueue() Initializes an empty queue object.
void enqueue(int val) Adds the element val to the back of the queue.
int dequeue() Removes and returns the element from the front of the queue.
int getMin() Retrieves the minimum element currently in the queue.
int getMax() Retrieves the maximum element currently in the queue.
Constraints

All operations must run in O(1) time.
1 ≤ enqueue.length, dequeue.length ≤
10
5
10 
5
 .
getMin, getMax, and dequeue will only be called on non-empty queues.
Example:

Input:
["MinMaxQueue", "enqueue", "enqueue", "enqueue", "getMin", "getMax", "dequeue", "getMin", "getMax"]
[[], [4], [2], [1], [], [], [], [], []]
Output:
[null, null, null, null, 1, 4, 4, 1, 2]
Explanation:

MinMaxQueue q = new MinMaxQueue();
q.enqueue(4); // Queue: [4]
q.enqueue(2); // Queue: [2, 4]
q.enqueue(1); // Queue: [1, 2, 4]
q.getMin(); // Returns 1. The minimum is 1.
q.getMax(); // Returns 4. The maximum is 4.
q.dequeue(); // Returns 4. Queue: [1, 2].
q.getMin(); // Returns 1. The minimum is 1.
q.getMax(); // Returns 2. The maximum is 2.

"""


"""
(This question is a variation of the LeetCode question 366. Find Leaves of Binary Tree. If you haven't completed that question yet, it is recommended to solve it first.)

Given the root of an N-ary tree, implement a function to remove all leaf nodes (nodes with zero children) from the tree each day, simultaneously. Repeat this process day by day:

On each day, after all current leaf nodes are removed, any nodes that become leaves (because their children were deleted) will be removed on the next day.
Continue until the entire tree has been removed, with the root being the final node removed.
Return a list days, where days[i] is a list of the node values removed on the 
(
i
+
1
)
th
(i+1) 
th
  day. The order of values within each sublist does not matter.

Example 1:

Input:

  1
/ | \
2 3 4
|
5
Output: [[5, 3, 4], [2], [1]]
Explanation:


Day 1: Remove nodes 5, 3, and 4 (all leaves).
Day 2: Node 2 is now a leaf, so it is removed.
Day 3: Node 1 is now the only remaining node and is removed.
Example 2:

Input:

1
|
2
|
3
|
4
Output: [[4], [3], [2], [1]]

Example 3:

Input:

      1
    / | \ 
   2  3  4 
 / |     |\ 
5  6    7  8 
  /|\    \
9 10 11  12
Output: [[5, 9, 10, 11, 3, 12, 8], [6, 7], [2, 4], [1]]
"""

"""
Design a miniature Unix find command inside an in-memory file system. The system should allow users to add files (with sizes and extensions) and later search any directory and sub-directory using size, extension, or name-prefix filters.

Given the following abstract Filter class:

abstract class Filter {
    // Returns true if the given file satisfies this filter's criterion
    abstract boolean apply(File file);
}
You need to implement three filter types and return a list of filenames that meet the provided filtering criteria. Your design should be extensible, allowing easy support for additional filter types in the future.

The system must support the following filter types:

Size Filter: Matches files whose size exceeds the threshold derived from filterParam. Valid units are "KB", "MB", and "GB".

For example, a filter with filterParam of "2MB" means files with size "5MB" and "1GB" are qualified, but "500KB" is not.
Extension Filter: Matches files whose extension (the substring after the dot) exactly equals filterParam.

For example, if filterParam is "xml", then "config.xml" qualifies, but "config.yml" does not.
Prefix Filter: Matches files whose base name (the substring before the dot) starts with filterParam.

For example, a filterParam of "doc" matches "doc.pdf" and "document.txt", but not "adoc.pdf".
Implement the FileSystem class:

FileSystem() Create an empty file system whose root path is "/".
String addFile(String fileName, String size, String path) Add a new file named fileName of the given size into a directory path.
On success, return the original fileName.
If a file with the same full name already exists in that directory, return an empty string.
Directory components that do not yet exist must be created automatically.
List<String> applyFilter(String path, String filterType, String filterParam) Recursively list all files under path that satisfy the filter. And you may return the qualified filenames in any order.
If filterType is "SIZE", then filterParam is a size string (e.g., "5MB"). Return files whose size is strictly greater than that value.
If filterType is "EXTENSION", then filterParam is an extension string (e.g., "xml"). Return files whose extension equals filterParam.
If filterType is "PREFIX", then filterParam is a filename prefix (ignore the extension). Return files whose base name starts with filterParam.
Constrains

File and directory names contain only lowercase letters plus exactly one dot (".") in each file name, separating name and extension.
Valid size units are "KB", "MB", "GB", and all size values are positive integers.
Path "/" denotes the root directory.
Example

Input:
["FileSystem","addFile","addFile","addFile","addFile","addFile","applyFilter","applyFilter","applyFilter","addFile"]

[[],["doc.pdf","5MB","/home/user/docs"],["img.jpg","2MB","/home/user/photos"],["script.sh","10KB","/home/user/bin"],["config.xml","1KB","/home/user/config"],["backup.zip","100MB","/home/user/backup"],["/home/user","SIZE","1MB"],["/home","EXTENSION","xml"],["/","PREFIX","doc"],["doc.pdf","10MB","/home/user/docs"]]

Output:
[null,"doc.pdf","img.jpg","script.sh","config.xml","backup.zip",["backup.zip","doc.pdf","img.jpg"],["config.xml"],["doc.pdf"],""]

Explanation:

FileSystem fs = new FileSystem();
fs.addFile("doc.pdf","5MB","/home/user/docs"); // Returns "doc.pdf".
fs.addFile("img.jpg","2MB","/home/user/photos"); // Returns "img.jpg".
fs.addFile("script.sh","10KB","/home/user/bin"); // Returns "script.sh".
fs.addFile("config.xml","1KB","/home/user/config"); // Returns "config.xml".
fs.addFile("backup.zip","100MB","/home/user/backup"); // Returns "backup.zip".
fs.applyFilter("/home/user","SIZE","1MB"); // Returns ["backup.zip","doc.pdf","img.jpg"] as all these files larger than 1 MB with the given directory path.
fs.applyFilter("/home","EXTENSION","xml"); // Returns ["config.xml]".
fs.applyFilter("/","PREFIX","doc"); // Returns ["doc.pdf"].
fs.addFile("doc.pdf","10MB","/home/user/docs"); // Returns "", since this is a duplicate filename in the given directory path.

Follow-up:
Extend the existing in-memory Unix find command so that users can cascade multiple filters in a single query using AND or OR logic.

Specifically, implement the FileSystem class with two new methods:

FileSystem() Create an empty file system whose root path is "/".
String addFile(String fileName, String size, String path) Add a new file named fileName of the given size into a directory path.
On success, return the original fileName.
If a file with the same full name already exists in that directory, return an empty string.
Directory components that do not yet exist must be created automatically.
(New) applyAndFilters(String path, List<List<String>> filterSpecs) Returns all files in any order that under path that satisfy every specified filter.
(New) applyOrFilters(String path, List<List<String>> filterSpecs) Returns all files in any order under path that satisfy at least one of the specified filters.
Constraints

1 ≤ filterSpecs.length ≤ 10.
Example

Input:
["FileSystem","addFile","addFile","addFile","addFile","addFile","applyAndFilters","applyOrFilters"]

[[], ["large.xml","10MB","/src"], ["small.xml","500KB","/src"], ["large.txt","15MB","/docs"], ["config.json","2MB","/config"], ["app.xml","8MB","/app/main"], ["/", [["SIZE","5MB"],["EXTENSION","xml"]]], ["/", [["SIZE","5MB"],["EXTENSION","json"]]]]

Output:
[null,"large.xml","small.xml","large.txt","config.json","app.xml",["large.xml","app.xml"],["large.xml","large.txt","config.json","app.xml"]]

Explanation:

FileSystem fs = new FileSystem();
fs.addFile("large.xml","10MB","/src"); // Returns "large.xml".
fs.addFile("small.xml","500KB","/src"); // Returns "small.xml".
fs.addFile("large.txt","15MB","/docs"); // Returns "large.txt".
fs.addFile("config.json","2MB","/config"); // Returns "config.json".
fs.addFile("app.xml","8MB","/app/main"); // Returns "app.xml".
fs.applyAndFilters("/", [["SIZE","5MB"],["EXTENSION","xml"]]); // Returns ["large.xml","app.xml"]. Both files exceed 5 MB and have extension "xml".
fs.applyOrFilters("/", [["SIZE","5MB"],["EXTENSION","json"]]); // Returns ["large.xml","large.txt","config.json","app.xml"]. Each file is larger than 5 MB or has the extension "json".
"""

"""
A builder has a project to repaint a row of houses on a street. Determine the number of ways to paint a row of n houses using k available colors (represented by integers 0 to k - 1). The painting must follow two rules:

No two adjacent houses can have the same color.
The color of the first house (firstHouseColor) and the color of the last house (lastHouseColor) are fixed and provided as input.
Calculate the total number of distinct ways to color the houses from index 1 to n - 2 (the intermediate houses) while adhering to these rules. Return 0 if no valid coloring exists.

Constraints:

1 <= n <= 10
1 <= k <= 10
k <= n
Example 1:

Input: n = 4, k = 3, firstHouseColor = 0, lastHouseColor = 2
Output: 3
Explanation: Given houses H₀, H₁, H₂, H₃ and available colors [0, 1, 2], where H₀ is fixed as color 0 and H₃ is fixed as color 2, the valid ways to paint the houses are [0, 1, 0, 2], [0, 2, 0, 2], and [0, 2, 1, 2].

Example 2:

Input: n = 5, k = 3, firstHouseColor = 1, lastHouseColor= 1
Output: 6

Example 3:

Input: n = 3, k = 2, firstHouseColor = 0, lastHouseColor= 1
Output: 0
"""

"""
Given a list of time blocks [person_id, start_day, end_day] where each block indicates a person's busy days (inclusive), generate an array of days where all people are free.

Each person_id is used only to group intervals for the same person, which should be merged accordingly. Days are 1-indexed, meaning the count starts from day 1.

Find all days when everyone is simultaneously available.

Example 1:

Input: intervals = [[1, 1, 2], [1, 4, 5]]
Output: [3]
Explanation: Person 1 is busy on days [1, 2] and [4, 5]. Therefore, free days should be [3].

Example 2:

Input: intervals = [[1, 1, 3], [2, 2, 4], [3, 3, 5]]
Output: []

Example 3:

Input: intervals = [[1, 1, 2], [2, 3, 4], [3, 5, 6]]
Output: []
Follow-up 1:
Given a list of time blocks [person_id, start_day, end_day], where each block indicates a person's busy days (inclusive), and an integer p representing the minimum number of people required to be free, determine all days when at least p people are simultaneously available.

Example 1:

Input: intervals = [[1, 1, 3], [2, 4, 5]], p = 1
Output: [1, 2, 3, 4, 5]
Explanation: At least 1 person is free every day.

Example 2:

Input: intervals = [[1, 1, 3], [2, 2, 5], [3, 4, 6]], p = 2
Output: [1, 6]

Example 3:

Input: intervals = [[1, 1, 3], [2, 2, 5], [3, 4, 6], [4, 6, 8]], p = 3
Output: [1, 7, 8]

Follow-up 2:
Given a list of time blocks [person_id, start_day, end_day], where each block indicates a person's busy days (inclusive), and two integers p and x, find all days that lie inside any stretch of at least x consecutive days during which at least p people are free.

Example 1:

Input: intervals = [[1, 2, 3], [1, 6, 7], [2, 4, 5], [2, 8, 9]], p = 1, x = 4
Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]
Explanation: The entire period forms a valid streak. Output starts at day 1.

Example 2:

Input: intervals = [[1, 1, 7], [2, 4, 8], [3, 6, 10], [4, 9, 12]], p = 3, x = 2
Output: [1, 2, 3, 11, 12]

Example 3:

Input: intervals = [[1, 1, 2], [1, 5, 7], [2, 3, 4], [2, 6, 8], [3, 5, 9]], p = 1, x = 2
Output: [1, 2, 3, 4, 5, 8, 9]
"""

"""
Given an array arr, where each element represents the distance you can fly on the 
i
th
i 
th
  day. You start with k units of energy, which is also your maximum energy capacity. Each day, you can either:

Fly: Use 1 unit of energy to fly arr[i] distance.
Rest: Recover 1 unit of energy, up to the maximum of k.
Determine the maximum total distance you can fly over all days.

Constraints:

1 <= arr.length <= 1000
1 <= arr[i] <= 1000
1 <= k <= 100
Example 1:

Input: arr = [5, 2, 8, 4, 3], k = 2
Output: 17
Explanation: The maximum fly distance is achieved by:

Day 0: Fly (energy 2 → 1, distance = 5)
Day 1: Rest (energy 1 → 2, distance = 5)
Day 2: Fly (energy 2 → 1, distance = 5 + 8 = 13)
Day 3: Fly (energy 1 → 0, distance = 13 + 4 = 17)
Day 4: Rest (energy 0 → 1, distance = 17)
Example 2:

Input: arr = [1, 2, 3, 4, 5], k = 3
Output: 13

Example 3:

Input: arr = [[10,1,1,10],2], k = 2
Output: 21


"""

"""
You are given a 2D list schedules representing employees' shift schedules. Each element is represented as a triplet containing the employee’s name, a start time, and an end time.

Your task is to merge overlapping shifts and generate a timeline of intervals. Each interval should display the start time, end time, and the list of employees working during that period. In the final output, employee names must appear in the order they first appeared in the input.

Constraints:

Each shift is given as [<name>, <start_time>, <end_time>] with start_time and end_time as integers.
Shifts may overlap, be adjacent, or separate.
An employee may have multiple shifts.
The output should exclude intervals with no active employees.
Example 1:

Input: schedules = [["Alice","1","5"],["Bob","2","6"],["Charlie","4","7"]]
Output: [["1","2","Alice"],["2","4","Alice","Bob"],["4","5","Alice","Bob","Charlie"],["5","6","Bob","Charlie"],["6","7","Charlie"]]
Explanation: The merged intervals are as follows:

The first interval [1,2] starts with only Alice working.
At time 2, Bob’s shift begins, so the interval [2,4] has both Alice and Bob.
At time 4, Charlie starts, which the interval [4,5] with all three employees.
When Alice’s shift ends at 5, the interval [5,6] consists of Bob and Charlie.
Finally, when Bob leaves at 6, the interval [6,7] shows only Charlie working.
Example 2:

Input: schedules = [["Alice","1","5"],["Bob","2","6"],["Alice","7","8"]]
Output: [["1","2","Alice"],["2","5","Alice","Bob"],["5","6","Bob"],["7","8","Alice"]]

Example 3:

Input: schedules = [["Charlie","1","5"],["Alice","2","6"],["Bob","4","7"]]
Output: [["1","2","Charlie"],["2","4","Charlie","Alice"],["4","5","Charlie","Alice","Bob"],["5","6","Alice","Bob"],["6","7","Bob"]]

"""

"""
Given an N x M grid representing a map with two cars, "a" and "b". Each car can move up, down, left, right, or stay in place at each step. The grid contains the following symbols:

".": Road (movable).
"#": Wall (impassable).
"a": Starting position of car a.
"b": Starting position of car b.
"A": Destination for car a.
"B": Destination for car b.
Your task is to determine whether both cars can reach their respective destinations (A for a, and B for b) at the same time, without colliding or blocking each other’s path during their movements.

Constraints:

Cars cannot occupy the same cell at the same time.
Cars cannot swap positions in one move (e.g., car a moves into car b’s position while b moves into a’s).
1
≤
N
,
M
≤
20
1≤N,M≤20.
Example 1:

Input: N = 1, M = 4, grid = [["a","B","A","b"]]

Output: false
Explanation: Cars "a" and "b" block each other’s paths.

Example 2:

Input: N = 3, M = 3, grid = [["b",".","A"],[".","a","."],[".",".","B"]]

Output: true

Example 3:

Input: N = 3, M = 3, grid = [["a","#","B"],["#","b","#"],["A","#","."]]

Output: false

"""

"""
You are given a 2D array of neighborhoods houses in a city, where each neighborhood (houses[i]) contains house numbers represented by integers. Rearrange the houses such that:

Each neighborhood is sorted in ascending order.
No two houses in the same neighborhood have the same number.
The capacity of each neighborhood (number of houses per row) remains unchanged.
Return the rearranged neighborhoods houses. If it is impossible to rearrange the houses so that each neighborhood meets the above conditions, return the original input unchanged. If there are multiple valid arrangements, returning any one of them is acceptable.

Constraints:

1
<
=
1<= houses.length 
<
=
100
<=100
1
<
=
1<= houses[i].length 
<
=
100
<=100
0
<
=
0<= houses[i][j] 
<
=
10
4
<=10 
4
 
Example 1:

Input: houses = [[1,2], [4,4,7,8], [4,9,9,9]]
Output: [[4,9], [1,4,8,9], [2,4,7,9]]
Explanation: This is one valid arrangement. Other possible answers are:

[[4,9],[1,2,4,9],[4,7,8,9]]
[[4,9],[1,4,7,9],[2,4,8,9]]
[[4,9],[2,4,7,9],[1,4,8,9]]
[[4,9],[2,4,8,9],[1,4,7,9]]
[[4,9],[4,7,8,9],[1,2,4,9]]
Example 2:

Input: houses = [[1,1,2], [2,3]]
Output: [[1,2,3], [1,2]]

Example 3:

Input: houses = [[5,5,5,4], [4,4,3], [3,2]]
Output: [[2,3,4,5], [3,4,5], [4,5]]
"""


"""
(This question is a variation of the LeetCode question 56. Merge Intervals. If you haven't completed that question yet, it is recommended to solve it first.)

Given two lists of intervals, where each interval is represented as a two-element array [start, end]. Each list contains non-overlapping intervals that are sorted by their start times.

You are asked to merge these two lists into a single list of non-overlapping intervals. If intervals from different lists overlap, they should be combined into a single continuous interval.

Constraints:

Both lists are sorted in non-descending order by the start time.
There is no overlap within each individual list.
Example 1:

Input: list1 = [[1, 5], [10, 14], [16, 18]], list2 = [[2, 6], [8, 10], [11, 20]]
Output: [[1, 6], [8, 20]]
Explanation: The intervals [1, 5] and [2, 6] are merged into [1, 6], while the remaining intervals combine to [8, 20].

Example 2:

Input: list1 = [[0, 2], [5, 10], [13, 23], [24, 25]], list2 = [[1, 5], [8, 12], [15, 24], [25, 26]]
Output: [[0, 12], [13, 26]]

Example 3:

Input: list1 = [[0, 10]], list2 = [[20, 100]]
Output: [[0, 10], [20, 100]]
"""

"""
(This question is a variation of the LeetCode question 282. Expression Add Operators. If you haven't completed that question yet, it is recommended to solve it first.)

Given an equation with no operators, you need to insert operators '+', '*', and parentheses '(', ')' only where necessary to form a valid expression that evaluates to the target value, and following standard arithmetic rules (parentheses, then multiplication, then addition).

The numbers must remain in their original order, and you can insert the operators anywhere between them. If at least one valid expression exists, return any one of them in the format of "<expression>=<target>". The output expression should be formatted with minimal parentheses (do not include unnecessary brackets). If no valid arrangement of operators yields the target, return "".

Constraints:

The left-hand side consists of one or more numbers.
You may use only the symbols '(', ')', '+', and '*' in addition to the given numbers.
The original order of numbers must not be altered.
Parentheses '(' and ')' may be added to override standard operator precedence, but they should only be included when required.
Example 1:

Input: numbers = [1,2,3,4,5], target = 105
Output: "(1+2)*(3+4)*5=105"
Explanation: (1 + 2) * (3 + 4) * 5 = 3 * 7 * 5 = 105. Other answers like "(1+((2+3)*4))*5=105" and "(1+2)*((3+4)*5)=105" are also correct.

Example 2:

Input: numbers = [2,3,4], target = 20
Output: "(2+3)*4=20"

Example 3:

Input: numbers = [2,3,5], target = 100
Output: ""
"""

"""
The city plans to allocate land for buildings and parking lots on a grid of equal-sized tiles. Each tile is either fixed as a parking lot ('P') or available for building ('-'). Some tiles may be marked as unusable (represented by 'X').

The planning rule requires that the height difference between any two adjacent tiles (up, down, left, or right) does not exceed one unit. Consequently, a building tile can be constructed taller if it is further from any parking lot—the building's maximum height is determined by the minimum number of moves needed to reach a parking lot.

Your task is to determine the maximum building height that can be planned, which is the greatest number of steps (or moves) required to reach any building tile from the nearest parking lot.

Constraints:

Adjacency includes only up, down, left, and right (diagonals are not considered).
The parking lot locations are fixed.
Unusable tiles ('X') cannot be used for buildings.
Example 1:


Input: [["P","-","-","X","-","-","-"],["-","X","-","-","-","X","-"],["-","-","X","-","-","-","-"],["X","-","-","-","X","-","P"]]
Output: 5
Explanation: The answer is 5 because it represents the maximum distance from any buildable tile ('-') such as (3,2), (3,3), or (0,4) to the nearest parking lot ('P'), and this is the highest height that the building can be built to meet all requirements.

Example 2:

Input: [[["P","X","-","-","-"],["-","X","X","X","-"],["-","-","X","-","-"],["-","X","X","X","-"],["-","-","-","X","P"]]]
Output: 6

Example 3:

Input: [[["P","-","-","X","-","-","-","-"],["-","X","-","X","-","X","-","-"],["-","-","-","-","X","-","-","-"],["-","X","X","-","-","X","X","-"],["-","-","-","-","-","-","-","-"],["-","X","-","X","-","-","X","-"],["-","-","-","-","X","-","-","-"],["-","-","-","-","-","-","-","P"]]]
Output: 11

"""

"""
Given a fixed-length list of data, where each element has a unique ID and three distinct properties. Two elements are considered duplicates if they share any of these properties.

Group elements based on shared properties, ensuring that each group contains all IDs connected through common properties. If an element has no shared properties with others, it forms its own separate group. You may return the groups in any order.

Constraints:

Each element has exactly one unique ID and three string properties.
The given input list should not be empty.
Example 1:

Input: data = [["id1","p1","p2","p3"], ["id2","p1","p4","p5"], ["id3","p6","p7","p8"]]
Output: [["id2","id1"],["id3"]]
Explanation:

E1 and E2 share the property "p1", so they form one group: ["id2","id1"].
E3 does not share any property with E1 or E2, so it stands alone as ["id3"].
Example 2:

Input: data = [["id1","p1","p2","p3"], ["id2","p1","p4","p5"], ["id3","p5","p7","p8"]]
Output: [["id1","id2","id3"]]

Example 3:

Input: data = [["id1","p1","p2","p3"],["id2","p3","p4","p5"],["id3","p6","p7","p8"],["id4","p8","p9","p10"],["id5","p11","p12","p13"]]
Output: [["id2","id1"],["id4","id3"],["id5"]]

"""

"""
When a user opens the search bar, the system should provide the most recent k search inputs as keyword recommendations. Each new search input should also be recorded and used for future recommendations. If a keyword is searched multiple times, only the most recent occurrence should be considered.

Implement the SearchHistory class:

SearchHistory(int capacity): Initialize the search history with a positive size capacity.
void add(String term): Add a search history to the cache. If the number of keys exceeds the capacity of this operation, evict the least recently used key.
List<String> getTopK(int k): Return the most recent k search inputs.
Constraints:

1 ≤ k ≤ 104
0 ≤ Number of search operations ≤ 105
Search keywords consist of lowercase and uppercase English letters.
Example:

Input:
["SearchHistory", "add", "add", "getTopK", "add", "getTopK","add","getTopK"]
[[3], ["paris"], ["tokyo"], [2], ["beijing"], [3], ["toronto"], [3]]
Output:
[null, null, null, ["tokyo","paris"], null, ["beijing", "tokyo", "paris"], null, ["toronto", "beijing", "tokyo"]
Explanation:

SearchHistory searchHistory = new SearchHistory(3); // Initialize with capacity 3
searchHistory.add("paris");
searchHistory.add("tokyo");
searchHistory.getTopK(2); // Returns ["tokyo,"paris"]
searchHistory.add("beijing");
searchHistory.getTopK(3); // Returns ["beijing","tokyo","paris"]
searchHistory.add("toronto");
searchHistory.getTopK(3); // Returns ["toronto","beijing","tokyo"]. Since the capacity is 3, "pairs" was evicted.

"""

"""
(This question is a variation of the LeetCode question 224. Basic Calculator. If you haven't completed that question yet, it is recommended to solve it first.)

Implement a function to evaluate a string expression containing nested "add" and "sub" functions. The "add" function adds its arguments, while the "sub" function subtracts the second argument from the first. Parse the expression and compute the correct integer result.

Note that the expression may include negative integers and spaces.

Constraints:

The input expression consists of only "add", "sub" functions, integers, parentheses "()", commas ",", and spaces.
The expression is always valid.
The numbers in the expression are all integers and in the range of [-105, 105].
Example 1:

Input: "add(add(1,3), sub(1,3))"
Output: 2
Explanation: It computes (1 + 3) + (1 - 3) = 2.

Example 2:

Input: "sub(1,3)"
Output: -2

Example 3:

Input: "add(-1, 3)"
Output: 2
"""


"""
You are given an array of coin denominations and an integer max, and you are asked to form every integer amount from 1 up to max using these coins.

Find the minimal number of coins used while still being able to create every value in the range [1, max]. Return -1 if these coin denominations cannot form any amount in that range.

Constraints:

1
≤
max
≤
10
5
1≤max≤10 
5
 .
Coin denominations are positive integers.
Example 1:

Input: coins = [1, 2, 5], max = 11
Output: 5
Explanation: With a total of 5 coins (at least 1 $1 coin, 2 $2 coins, and 2 $5 coins), we can cover all amounts from 1 to 11.

$1: 1 * $1
$2: 1 * $2
$3: 1 * $1 + 1 * $2
$4: 2 * $2
$5: 1 * $1 + 2 * $2
$6: 1 * $5 + 1 * $1
$7: 1 * $5 + 1 * $2
$8: 1 * $1 + 1 * $2 + 1 * $5
$9: 1 * $5 + 2 * $2
$10: 2 * $5
$11: 2 * $5 + 1 * $1
Across all these amounts, we only need 5 coins in total.

Example 2:

Input: coins = [1, 3, 4], max = 6
Output: 4

Example 3:

Input: coins = [2, 5], max = 10
Output: -1
"""

"""
(This question is a variation of the LeetCode question 39. Combination Sum. If you haven't completed that question yet, it is recommended to solve it first.)

Given a list of positive integers and a target number k, write a function that returns true if there exists a subset of nums that adds up to k, and false otherwise. Note that numbers can appear more than once in the list.

Constraints:

1 <= nums.length <= 1000
1 <= nums[i] <= 
10
6
10 
6
 
1 <= k <= 
10
9
10 
9
 
Example 1:

Input: nums = [12, 1, 61, 5, 9, 2], k = 24
Output: true
Explanation: There exists a subset [12, 9, 2, 1] that sums up to 24.

Example 2:

Input: nums = [3, 34, 4, 12, 5, 2, 2], k = 9
Output: true
Explanation: There exists a subset [4, 5] that sums up to 9.

Example 3:

Input: nums = [5, 3, 9, 2, 7], k = 6
Output: false

"""

"""
Given a 2D keyboard represented by a m × n character matrix, a maximum jump distance, and a target word, determine if you can type the word by moving between characters without exceeding this distance. The distance here is calculated as the Manhattan distance: 
∣
x
1
−
x
2
∣
+
∣
y
1
−
y
2
∣
∣x1−x2∣+∣y1−y2∣.

Constraints:

Jump distance ≥ 0
The word can have up to 1000 characters.
Example 1:

Input:
jumpDistance = 2
keyboard = [["Q","X","P","L","E"],
            ["W","A","C","I","N"]]
word = "PENCIL"
Output: true
Explanation:

Start from 'P' at position (0, 2).
Jump to 'E' at (0, 4), distance = |0-0| + |4-2| = 2.
Jump to 'N' at (1, 4), distance = |1-0| + |4-4| = 1.
Jump to 'C' at (1, 2), distance = |1-1| + |2-4| = 2.
Jump to 'I' at (1, 3), distance = |1-1| + |3-2| = 1.
Finally, jump to 'L' at (0, 3), distance = |0-1| + |3-3| = 1.
All jumps stay within the maximum distance of 2.
Example 2:

Input:
jumpDistance = 4
keyboard = [["T","E","C","H"],
            ["W","A","V","E"],
            ["X","Y","Z","M"],
            ["N","O","P","Q"]]
word = "TECHWAVE"
Output: true

Example 3:

Input:
jumpDistance = 2
keyboard = [["C","A","T","X","O","J","W","Z"],
            ["O","M","B","V","R","T","U","P"],
            ["M","U","R","P","Q","G","D","R"],
            ["P","I","S","R","A","C","T","G"],
            ["U","O","L","E","M","S","P","V"],
            ["T","U","Q","H","I","C","R","A"],
            ["E","X","Z","B","T","D","Y","N"],
            ["F","G","R","G","A","M","P","O"]]
word = "COMPUTERGRAPH"
Output: false


"""



"""
Given an algebraic expression containing variables, parentheses, addition ("+"), and subtraction ("-") operators, simplify the expression by removing all unnecessary parentheses and correctly adjusting the signs of the terms. The simplified expression should maintain the correct order of operations and accurately represent the original expression's value.

Constraints:

1 <= expression.length <= 
10
5
10 
5
 
The expression consists of lowercase English letters, "+", "-", "(", ")", and no other characters.
Example 1:

Input: "a-(b+c)"
Output: "a-b-c"
Explanation: Removing the parentheses and distributing the negative sign results in "a-b-c".

Example 2:

Input: "a-(-b-c)"
Output: "a+b+c"

Example 3:

Input: "(x+y)-z"
Output: "x+y-z"


"""

"""
(This question is a variation of the LeetCode question 486. Predict the Winner. If you haven't completed that question yet, it is recommended to solve it first.)

Two players take turns selecting balls from a line. At the start of the game, both players have a score of 0. On each turn, a player can choose to pick either one or two balls from the remaining line. Each ball has an integer value, which can be either positive or negative. Once a player picks a ball, it cannot be selected again by either player. Both players aim to maximize their own total profit by the end of the game. The game ends when all the balls have been picked.

After all selections are made, calculate and return the maximum difference between Player One's total profit and Player Two's total profit.

Constraints:

1 ≤ nums.length ≤ 
10
5
10 
5
 
−
10
4
−10 
4
 ≤ nums[i] ≤ 
10
4
10 
4
 
Example 1:

Input: [1, -1, -3, 1, 2, 4]
Output: 2
Explanation:

Player One picks 1 and -1, total = 0.
Player Two picks -3, total = -3.
Player One picks 1 and 2, total = 3.
Player Two picks 4, total = 1.
After all selections, player one total = 3, player two total = 1. The maximum difference is 2.
Example 2:

Input: [1, 2, 3, 4]
Output: 0

Example 3:

Input: [4, -1, 2, -3, 5]
Output: 5
"""


"""
Given the roots of two Binary Search Trees (BSTs) containing integer values, find the greatest common integer present in both trees. If there is no common integer, return -1.

Constraints:

The number of nodes in both trees is in the range 
[
1
,
10
5
]
[1,10 
5
 ].
−
10
9
≤
Node.val
≤
10
9
−10 
9
 ≤Node.val≤10 
9
 
Both trees are valid BSTs.
Example 1:

Input: root1 = [5, 3, 7], root2 = [9, 5, 12, null, 7]
Output: 7
Explanation:  The common integers are 5 and 7. The greatest common integer is 7.

Tree 1:
image

Tree 2:
image

Example 2:

Input: root1 = [10, 5, 15, 3, 7, 12, 18], root2 = [20, 15, 25, 10, 18]
Output: 18

Example 3:

Input: root1 = [9, 5, 12, 3, 7, 10], root2 = [7, 3, 10, null, 5, null, 13]
Output: 10


"""


"""
Consider a bank with an initial amount of money and a series of transactions. Each transaction is represented as an integer in an array: positive values indicate deposits and negative values indicate withdrawals. The bank can choose which customer to serve first and can skip any number of customers initially. However, once the bank starts serving, it must continue sequentially until serving a customer becomes impossible due to insufficient balance.

Maximize the total number of customers the bank can serve.

Constraints:

The initial amount is a non-negative integer.
Transactions array contains integers that can be positive or negative.
The bank must serve customers sequentially once started.
Example 1:

Input: initialAmount = 1, transactions = [1, -3, 5, -2, 1]
Output: 3
Explanation: Starting with the deposit of 5: 1 + 5 = 6, 6 - 2 = 4, 4 + 1 = 5. Three customers served.

Example 2:

Input: initialAmount = 5, transactions = [-2, -3, -1, -4]
Output: 2
Explanation: Starting from the beginning, the bank can serve two customers: 5 - 2 = 3, 3 - 3 = 0.

Example 3:

Input: initialAmount = 10, transactions = [5, -6, 3, -2, 4]
Output: 5


"""