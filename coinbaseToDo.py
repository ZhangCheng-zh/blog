"""
Given a list of currency relationships with exchange values (e.g., BGP → USD: 109.0). Find the best exchange rate from from currency to to currency with the following assumptions:

The rates are bi-directional. If the rate from A to B is 
r
r, the rate from B to A can be calculated as 
1
/
r
1/r.
The goal is to find the maximum achievable exchange rate, which is the highest value obtained by multiplying the rates along a valid exchange path.
If the conversion is not possible, return -1.
Implement the CurrencyConverter class:

CurrencyConverter(String[] fromArr, String[] toArr, double[] rateArr) Initialize the CurrencyConverter class with currency pairs and exchange rates.
getBestRate(String from, String to) Return the best exchange rate that can be obtained from from currency to to currency.
Constraints:

1 ≤ fromArr.length, toArr.length, rateArr.length ≤ 1000
0 < rateArr[i] ≤ 103
All currency names consist of English letters and have a length between 1 and 10
Example 1:

Input:
["CurrencyConverter", "getBestRate", "getBestRate", "getBestRate", "getBestRate"]

[[["GBP", "USD", "USD", "USD", "CNY"], ["JPY", "JPY", "GBP", "CAD", "EUR"], [155.0, 112.0, 0.9, 1.3, 0.14]], ["USD", "JPY"], ["JPY", "BGP"], ["XYZ", "GBP"], ["CNY", "CAD"]]

Output:
[null, 139.5, 0.00803, -1.0, -1.0]

Explanation:

CurrencyConverter currencyConverter = new CurrencyConverter(fromArr, toArr, rateArr);
currencyConverter.getBestRate("USD", "JPY"); // Return 139.5, the best exchange path is an indirect path USD → BGP → JPY = (1/0.9) * 155 = 139.5, better than the direct paths like USD → JPY = 112.0
currencyConverter.getBestRate("JPY", "BGP"); // Return 0.00803, the best exchange path is JPY→ USD → BGP.
currencyConverter.getBestRate("XYZ", "BGP"); // Returns -1.0, because "XYZ" doesn't exist in the currency array.
currencyConverter.getBestRate("CNY", "CAD"); // returns -1.0, because no exchange path exists from "CNY" to "CAD".
"""


"""
Introduce operations for adding workers, registering their entering or leaving the office and retrieving information about the amount of time that they have worked.

boolean addWorker(String workerId, String position, int compensation) — should add the workerId to the system and save additional information about them: their position and compensation.

If the workerId already exists, nothing happens and this operation should return "false".
If the workerId was successfully added, return "true".
workerId and position are guaranteed to contain only English letters and spaces.
String registerWorker(String workerId, int timestamp) — should register the time when the workerId entered or left the office. The time is represented by the timestamp. Note that registerWorker operation calls are given in the increasing order of the timestamp parameter.

If the workerId doesn't exist within the system, nothing happens and this operation should return "invalid_request".
If the workerId is not in the office, this operation registers the time when the workerId entered the office.
If the workerId is already in the office, this operation registers the time when the workerId left the office.
If the workerId's entering or leaving time was successfully registered, return "registered".
int get(String workerId) — should return a number representing the total calculated amount of time that the workerId spent in the office.

The amount of time is calculated using finished working sessions only. It means that if the worker has entered the office but hasn't left yet, this visit is not considered in the calculation.
If the workerId doesn't exist within the system, return -1.
Example:

Input:
["OfficeManager", "addWorker", "addWorker", "registerWorker", "registerWorker", "get", "registerWorker", "registerWorker", "registerWorker", "get", "get", "registerWorker"]
[[], ["Ashley", "Middle Developer", 150], ["Ashley", "Junior Developer", 100], ["Ashley", 10], ["Ashley", 25], ["Ashley"], ["Ashley", 40], ["Ashley", 67], ["Ashley", 100], ["Ashley"], ["Walter"], ["Walter", 120]]

Output:
[null, true, false, "registered", "registered", 15, "registered", "registered", "registered", 42, -1, "invalid_request"]

Explanation:

OfficeManager officeManager = new OfficeManager();
officeManager.addWorker("Ashley", "Middle Developer", 150); // Returns true.
officeManager.addWorker("Ashley", "Junior Developer", 100); // Returns false. The same worker ID already exists within the system.
officeManager.registerWorker("Ashley", 10); // Returns "registered". "Ashley" entered the office at timestamp 10.
officeManager.registerWorker("Ashley", 25); // Returns "registered". "Ashley" left the office at timestamp 25.
officeManager.get("Ashley"); // Returns 15. "Ashley" spent 25 - 10 = 15 time units in the office.
officeManager.registerWorker("Ashley", 40); // Returns "registered".
officeManager.registerWorker("Ashley", 67); // Returns "registered".
officeManager.registerWorker("Ashley", 100); // Returns "registered".
officeManager.get("Ashley"); // Returns 42. "Ashley" spent (25 - 10) + (67 - 40) = 42 time units in the office.
officeManager.get("Walter"); // Returns -1. id "Walter" was never added to the system.
officeManager.registerWorker("Walter", 120); // Returns "invalid_request". "Walter" was never added to the system.

Follow-up 1:
Introduce an operation to retrieve ordered statistics about the workers.

String topNWorkers(int n, String position) — should return the string representing the IDs of the top n workers with the given position sorted in descending order by the total time spent in the office.

The amount of time is calculated using finished working sessions only. In the case of a tie, workers must be sorted in alphabetical order of their IDs.
The returned string should be in the following format: "workerId1(timeSpentInOffice1), workerId2(timeSpentInOffice2), workerIdn(timeSpentInOfficeN)"
If fewer than n workers with the given position exist within the system, then return all IDs in the described format.
If there are no workers with the given position with at least one time period registered, return an empty string.
Note that if a worker exists within the system and doesn't have any finished periods of being in the office, their time spent in the office is considered to be 0.

Example:

Input:
["OfficeManager", "addWorker", "addWorker", "addWorker", "registerWorker", "registerWorker", "registerWorker", "registerWorker", "registerWorker", "topNWorkers", "topNWorkers", "registerWorker", "registerWorker", "registerWorker", "topNWorkers", "topNWorkers"]
[[], ["John", "Junior Developer", 120], ["Jason", "Junior Developer", 120], ["Ashley", "Junior Developer", 120], ["John", 100], ["John", 150], ["Jason", 200], ["Jason", 250], ["Jason", 275], [5, "Junior Developer"], [1, "Junior Developer"], ["Ashley", 400], ["Ashley", 500], ["Jason", 575], [5, "Junior Developer"], [5, "Middle Developer"]]

Output:
[null, true, true, true, "registered", "registered", "registered", "registered", "registered", "Jason(50),  John(50),  Ashley(0)", "Jason(50)", "registered", "registered", "registered", "Jason(350), Ashley(100), John(50)", ""]

Explanation:

OfficeManager manager = new OfficeManager();
manager.addWorker("John", "Junior Developer", 120); // Returns true.
manager.addWorker("Jason", "Junior Developer", 120); // Returns true.
manager.addWorker("Ashley", "Junior Developer", 120); // Returns true.
manager.registerWorker("John", 100); // Returns "registered".
manager.registerWorker("John", 150); // Returns "registered". Now "John" has 50 time units spent in the office.
manager.registerWorker("Jason", 200); // Returns "registered".
manager.registerWorker("Jason", 250); // Returns "registered". Now "Jason" has 50 time units spent in the office.
manager.registerWorker("Jason", 275); // Returns "registered". "Jason" entered the office at timestamp 275.
manager.topNWorkers(5, "Junior Developer"); // Returns "Jason(50), John(50), Ashley(0)". "Jason" goes before "John" alphabetically.
manager.topNWorkers(1, "Junior Developer"); // Returns "Jason(50)".
manager.registerWorker("Ashley", 400); // Returns "registered".
manager.registerWorker("Ashley", 500); // Returns "registered". Now "Ashley" has 100 time units spent in the office.
manager.registerWorker("Jason", 575); // Returns "registered". "Jason" left the office and now has 50 + (575 - 275) = 350 time units spent in the office.
manager.topNWorkers(5, "Junior Developer"); // Returns "Jason(350), Ashley(100), John(50)".
manager.topNWorkers(5, "Middle Developer"); // Returns "". There are no workers with the position "Middle Developer".


Follow-up 2:
Introduce operations to promote workers and calculate salaries.

String promote(String workerId, String newPosition, String newCompensation, int startTimestamp) — should register a new position and new compensation for the workerId.
newPosition is guaranteed to be different from the current worker's position.
New position and new compensation are active from the moment of the first entering the office after or at startTimestamp. In other words, the first time period of being in office for the newPosition starts at or after startTimestamp.
startTimestamp is guaranteed to be greater than the timestamp parameter of the last registerWorker call for any worker.
If the promote operation is called repeatedly for the same workerId before they entered the office with the newPosition, nothing happens, and this operation should return "invalid_request".
If workerId doesn't exist within the system, nothing happens, and this operation should return "invalid_request".
If the worker's promotion was successfully registered, return "success".
Note:

topNWorkers operation should take into account only the worker's current position into account.

get operation should return the total amount of time across all the worker's past and current positions.

int calcSalary(String workerId, int startTimestamp, int endTimestamp) — should calculate net salary that workerId has earned for the time period between startTimestamp and endTimestamp.

No restrictions are applied to startTimestamp and endTimestamp (except that it is guaranteed that endTimestamp ≥ startTimestamp). Workers are only paid for the time they were present in the office.
The amount of time is calculated using finished working sessions only.
For any finished working session [sessionStartTimestamp, sessionEndTimestamp], salary is calculated as:salary = (sessionEndTimestamp - sessionStartTimestamp) × compensationDuringPeriod
Note that compensationDuringPeriod may differ for different periods, because workers may be promoted.
If workerId doesn't exist within the system, nothing happens and this operation should return -1.
Example:

Input:
["OfficeManager", "addWorker", "registerWorker", "registerWorker", "promote", "registerWorker", "promote", "registerWorker", "registerWorker", "calcSalary", "topNWorkers", "registerWorker", "get", "topNWorkers", "topNWorkers", "calcSalary", "calcSalary"]
[[], ["John", "Middle Developer", 200], ["John", 100], ["John", 125], ["John", "Senior Developer", "500", 200], ["John", 150], ["John", "Senior Developer", "350", 250], ["John", 300], ["John", 325], ["John", 0, 500], [3, "Senior Developer"], ["John", 400], ["John"], [10, "Senior Developer"], [10, "Middle Developer"], ["John", 110, 350], ["John", 900, 1400]]

Output:
[null, true, "registered", "registered", "success", "registered", "invalid_request", "registered", "registered", 35000, "John(0)", "registered", 250, "John(75)", "", 45500, 0]

Explanation:

OfficeManager officeManager = new OfficeManager();
officeManager.addWorker("John", "Middle Developer", 200); // Returns true. Adds John to the system
officeManager.registerWorker("John", 100); // Returns "registered". John enters the office
officeManager.registerWorker("John", 125); // Returns "registered".Worker "John" has 25 time units spent in the office
officeManager.promote("John", "Senior Developer", "500", 200); // Returns "success". At timestamp 200 new position and new compensation will be granted to "John"
officeManager.registerWorker("John", 150); // Returns "registered". John enters. Promotion is not yet active (150 < 200).
officeManager.promote("John", "Senior Developer", "350", 250); // Returns "invalid_request". "John" has an active new position registration, which is not been applied yet
officeManager.registerWorker("John", 300); // Returns "registered". "John" leaves the office. Now this worker has 25 + (300 - 150) = 175 time units spent in the office
officeManager.registerWorker("John", 325); // Returns "registered". "John" left the office at timestamp 325. It is greater than the new position's starting timestamp 200, so the new compensation is assigned
officeManager.calcSalary("John", 0, 500); // Returns 35000. During the period [0, 500], there were two time periods when "John" was in the office: [100, 125], [150, 300] as "Middle Developer" with compensation = 200. Salary is calculated as (125 - 100) * 200 + (300 - 150) * 200 = 35000.
officeManager.topNWorkers(3, "Senior Developer"); // Returns "John(0)". John's current position is Senior Developer, but he has 0 completed work time in this role so far
officeManager.registerWorker("John", 400); // Returns "registered". John leaves, completing his first session [325, 400] as a Senior Developer
officeManager.get("John"); // Returns 250. This is his total time across all roles: (125-100) + (300-150) + (400-325) = 25 + 150 + 75 = 250
officeManager.topNWorkers(10, "Senior Developer"); // Returns "John(75)".
officeManager.topNWorkers(10, "Middle Developer"); // Returns "". No one is currently a Middle Developer, so the result is empty
officeManager.calcSalary("John", 110, 350); // Returns 45500. It sums salary from overlapping parts of 3 sessions: (125 - 110) * 200 + (300 - 150) * 200 + (350 - 325) * 500 = 45500
officeManager.calcSalary("John", 900, 1400); // Returns 0.


Follow-up 3:
Introduce an operation for setting double-paid periods.

void setDoublePaid(int startTimestamp, int endTimestamp) — should set the time period between startTimestamp and endTimestamp to be a double-paid period.
No restrictions are applied to startTimestamp and endTimestamp, except that it is guaranteed that endTimestamp > startTimestamp ≥ 0.
Multiple double-paid periods can be set. Double-paid periods may overlap but they will still be double-paid only.
Note:

calcSalary operation should take double-paid periods into account.
Example:

Input:
[null, true, "registered", "registered", "success", "registered", "invalid_request", "registered", "registered", 35000, "John(0)", "registered", 250, "John(75)", "", 45500, 0]
[null, true, "registered", "registered", "success", "registered", "invalid_request", "registered", "registered", 35000, "John(0)", "registered", 250, "John(75)", "", 45500, 0]

Output:
[null, true, "registered", "registered", "registered", "registered", "registered", "registered", null, null, null, 17000, 44000]

Explanation:

OfficeManager manager = new OfficeManager();
manager.addWorker("John", "Middle Developer", 100); // Returns true.
manager.registerWorker("John", 100); // Returns "registered".
manager.registerWorker("John", 200); // Returns "registered". Now "John" has 100 time units spent in the office: [100, 200].
manager.registerWorker("John", 500); // Returns "registered".
manager.registerWorker("John", 600); // Returns "registered". Now "John" has 200 time units spent in the office: [100, 200], [500, 600].
manager.registerWorker("John", 900); // Returns "registered".
manager.registerWorker("John", 1000); // Returns "registered". Now "John" has 300 time units spent in the office: [100, 200], [500, 600], [900, 1000].
manager.setDoublePaid(50, 170); // Returns null. Now there is one double-paid period, which is [50, 170].
manager.setDoublePaid(530, 650); // Returns null. Now there are two double-paid periods: [50, 170] and [530, 650].
manager.setDoublePaid(580, 900); // Returns null. Now there are three double-paid periods: [50, 170], [530, 650], and [580, 900]. There are two overlapping double-paid periods: [530, 650], [580, 900]. As overlapping doesn't affect the amount to be paid, we may think of it as a single double-paid period [530, 900]. Thus, we will consider two double-paid periods: [50, 170], [530, 900].
manager.calcSalary("John", 0, 250); // Returns 17000. During the period [0, 250], there was one period of time when "John" was in the office: [100, 200]. There is one double-paid period affecting this period of time: [50, 170]. So, time period [100, 170] is double paid, and time period [170, 200] is not. Salary is calculated as (170 - 100) * 100 * 2 + (200 - 170) * 100 = 17000
manager.calcSalary("John", 0, 1500); // Returns 44000. Following the same logic as in the previous operation, salary is calculated as (170 - 100) * 100 * 2 + (200 - 170) * 100 + (530 - 500) * 100 + (600 - 530) * 100 * 2 + (1000 - 900) * 100 = 44000

"""


"""
The cloud storage system should support operations to add files, copy files, and retrieve files stored on the system.

boolean addFile(String name, int size) — should add a new file name to the storage. size is the amount of memory required in bytes.

The current operation fails if a file with the same name already exists.
Returns true if the file was added successfully or false otherwise.
boolean copyFile(String nameFrom, String nameTo) — should copy the file at nameFrom to nameTo.

The operation fails if nameFrom points to a file that does not exist or points to a directory.
The operation fails if the specified file already exists at nameTo.
Returns true if the file was copied successfully or false otherwise.
int getFilesize(String name) — should return the size of the file name if it exists, or -1 otherwise.

Constraints:

Each file name name is a non-empty string and may include any visible ASCII characters (including /).
There is no separate concept of directories; every name is treated as a distinct file.
At most 
10
5
10 
5
  operations will be performed.
All file sizes size fit within a 32-bit signed integer.
Example

Input:
["CloudStorage", "addFile", "copyFile", "copyFile", "addFile", "copyFile", "getFileSize", "getFileSize"]

[[], ["/dir1/dir2/file.txt", 10], ["/not-existing.file", "/dir1/file.txt"], ["/dir1/dir2/file.txt", "/dir1/file.txt"], ["/dir1/file.txt", 15], ["/dir1/file.txt", "/dir1/dir2/file.txt"], ["/dir1/file.txt"], ["/not-existing.file"]]

Output:
[null, true, false, true, false, false, 10, -1]

Explanation:

CloudStorage cloudStorage = new CloudStorage();
cloudStorage.addFile("/dir1/dir2/file.txt", 10); // Returns true; adds file "/dir1/dir2/file.txt" of 10 bytes.
cloudStorage.copyFile("/not-existing.file", "/dir1/file.txt"); // Returns false; the file "/not-existing.file" does not exist.
cloudStorage.copyFile("/dir1/dir2/file.txt", "/dir1/file.txt"); // Returns true; adds file "/dir1/file.txt" of 10 bytes.
cloudStorage.addFile("/dir1/file.txt", 15); // Returns false; the file "/dir1/file.txt" exists already.
cloudStorage.copyFile("/dir1/file.txt", "/dir1/dir2/file.txt"); // Returns false; the file "/dir1/dir2/file.txt" exists already.
cloudStorage.getFileSize("/dir1/file.txt"); // Returns 10. The file size.
cloudStorage.getFileSize("/not-existing.file"); // Returns -1; the file "/not-existing.file" does not exist.

Follow-up 1:
Implement support for retrieving file names by searching directories via prefixes and suffixes.

List<String> findFile(String prefix, String suffix) — should search for files with names starting with prefix and ending with suffix.
Returns a list of strings representing all matching files in this format:["<name1>(<size1>)", "<name2>(<size2>)", ...], The output should be sorted in descending order of file sizes or, in the case of ties, lexicographically.
If no files match the required properties, return an empty list.
Constraints:

1
1 ≤ total number of files ≤ 
10
5
10 
5
 
0
0 ≤ file size ≤ 
2
×
10
9
2×10 
9
 
File names are unique.
Scanning all stored files for findFile is acceptable.
Example:

Input:
["CloudStorage", "addFile", "addFile", "addFile", "copyFile", "findFile", "findFile", "findFile"]

[[], ["/root/dir/another_dir/file.mp3", 10], ["/root/file.mp3", 5], ["/root/music/file.mp3", 7], ["/root/music/file.mp3", "/root/dir/file.mp3"], ["/root", ".mp3"], ["/root", "file.txt"], ["/dir", "file.mp3"]]

Output:
[null, true, true, true, true, ["/root/dir/another_dir/file.mp3(10)", "/root/dir/file.mp3(7)", "/root/music/file.mp3(7)", "/root/file.mp3(5)"], [], []]

Explanation:

CloudStorage cloudStorage = new CloudStorage();
cloudStorage.addFile("/root/dir/another_dir/file.mp3", 10); // Returns true.
cloudStorage.addFile("/root/file.mp3", 5); // Returns true.
cloudStorage.addFile("/root/music/file.mp3", 7); // Returns true.
cloudStorage.copyFile("/root/music/file.mp3", "/root/dir/file.mp3"); // Returns true.
cloudStorage.findFile("/root", ".mp3"); // Returns ["/root/dir/another_dir/file.mp3(10)","/root/dir/file.mp3(7)","/root/music/file.mp3(7)", "/root/file.mp3(5)"]
cloudStorage.findFile("/root", "file.txt"); // Returns []; there is no file with the prefix "/root" and suffix "file.txt"
cloudStorage.findFile("/dir", "file.mp3"); // Returns []; there is no file with the prefix "/dir" and suffix "file.mp3"


Follow-up 2:
Implement support for different users sending queries to the system. All users share a common filesystem in the cloud storage, but each user is assigned an individual storage capacity limit.

boolean addUser(String userId, int capacity) — should add a new user to the system, with capacity as their storage limit in bytes.

The total size of all files owned by userId cannot exceed capacity. The operation fails if a user with userId already exists.
Returns true if a user with userId is successfully created, or false otherwise.
int addFileBy(String userId, String name, int size) — should behave in the same way as the addFile from the previous questions, but the added file should be owned by the user with userId.

A new file cannot be added to the storage if doing so will exceed the user's capacity limit.
Returns the remaining storage capacity for userId if the file is successfully added or -1 otherwise.
Note that all queries calling the addFile operation implemented during the previous questions are run by the user with userId = "admin", who has unlimited storage capacity. Also, assume that the copyFile operation preserves the ownership of the original file.

int updateCapacity(String userId, int capacity) — should change the maximum storage capacity for the user with userId.
If the total size of all user's files exceeds the new capacity, the largest files (sorted lexicographically in case of a tie) should be removed from the storage until the total size of all remaining files no longer exceeds the new capacity.
Returns the number of removed files, or -1 if a user with userId does not exist.
Constraints:

1
1 ≤ length of userId, name ≤ 
100
100
1
1 ≤ capacity, size ≤ 
10
9
10 
9
 
All userId values are case-sensitive.
All file name values are unique globally.
No file's size exceeds its owner's capacity.
The user "admin" cannot be created or removed.
Example:

Input:
["CloudStorage", "addUser", "addUser", "addUser", "addFileBy", "addFileBy", "addFileBy", "copyFile", "copyFile", "addFileBy", "addFile", "addFileBy", "addFileBy", "addFileBy", "updateCapacity", "updateCapacity", "updateCapacity"]

[[], ["user1", 125], ["user1", 100], ["user2", 100], ["user1", "/dir/file.big", 50], ["user1", "/file.med", 30], ["user2", "/file.med", 40], ["/file.med", "/dir/another/file.med"], ["/file.med", "/dir/another/another/file.med"], ["user1", "/dir/file.small", 10], ["/dir/admin_file", 200], ["user1", "/dir/file.small", 5], ["user1", "/my_folder/file.huge", 100], ["user3", "/my_folder/file.huge", 100], ["user1", 300], ["user1", 50], ["user2", 1000]]

Output:
[null, true, false, true, 75, 45, -1, true, false, 5, true, -1, -1, -1, 0, 2, 0]

Explanation:

CloudStorage cloudStorage = new CloudStorage();
cloudStorage.addUser("user1", 125); // Returns true; creates user "user1" with 125 bytes capacity.
cloudStorage.addUser("user1", 100); // Returns false; "user1" already exists.
cloudStorage.addUser("user2", 100); // Returns true; creates user "user2" with 100 bytes capacity.
cloudStorage.addFileBy("user1", "/dir/file.big", 50); // Returns 75; file added for "user1", remaining capacity: 75.
cloudStorage.addFileBy("user1", "/file.med", 30); // Returns 45; file added for "user1", remaining capacity: 45.
cloudStorage.addFileBy("user2", "/file.med", 40); // Returns -1; file named "/file.med" already exists and is owned by "user1".
cloudStorage.copyFile("/file.med", "/dir/another/file.med"); // Returns true; copying preserves the file owner. After copying, "user1" has 15 capacity left.
cloudStorage.copyFile("/file.med", "/dir/another/another/file.med"); // Returns false; "user1" does not have enough storage capacity left to perform the copying operation.
cloudStorage.addFileBy("user1", "/dir/file.small", 10); // Returns 5; file added for "user1", remaining capacity: 5.
cloudStorage.addFile("/dir/admin_file", 200); // Returns true; this operation is done by "admin" with unlimited capacity.
cloudStorage.addFileBy("user1", "/dir/file.small", 5); // Returns -1; the file "/dir/file.small" already exists.
cloudStorage.addFileBy("user1", "/my_folder/file.huge", 100); // Returns -1; "user1" does not have enough storage capacity left to add this file
cloudStorage.addFileBy("user3", "/my_folder/file.huge", 100); // Returns -1; "user3" doesn't exist.
cloudStorage.updateCapacity("user1", 300); // Returns 0; all files owned by "user1" can fit into the new capacity of 300 bytes.
cloudStorage.updateCapacity("user1", 50); // Returns 2; the files "/dir/file.big" and "/dir/another/file.med", should be deleted so the remaining files owned by "user1" can fit into the new capacity of 50 bytes.
cloudStorage.updateCapacity("user2", 1000); // Returns 0.


Follow-up 3:
Implement support for file compression.

int compressFile(String userId, String name) — should compress the file name if it belongs to userId.
The compressed file should be replaced with a new file named <name>.COMPRESSED.
The size of the newly created file should be equal to half of the original file.
The size of all files is guaranteed to be even, so there should be no fractional calculations.
It is also guaranteed that name for this operation never points to a compressed file — i.e., it never ends with .COMPRESSED.
Compressed files should be owned by userId — the owner of the original file.
Returns the remaining storage capacity for userId if the file was compressed successfully or -1 otherwise.
Note that because file names can only contain lowercase letters, compressed files cannot be added via addFile.

It is guaranteed that all copyFile operations will preserve the suffix .COMPRESSED.

int decompressFile(String userId, String name) — should revert the compression of the file name if it belongs to userId.
It is guaranteed that name for this operation always ends with .COMPRESSED.
If decompression results in the userId exceeding their storage capacity limit or a decompressed version of the file with the given name already exists, the operation fails.
Returns the remaining capacity of userId if the file was decompressed successfully or -1 otherwise.
Constraints:

Each file name is unique.
1
1 ≤ total number of files ≤ 
10
5
10 
5
 .
1
1 ≤ number of users ≤ 
10
5
10 
5
 .
1
1 ≤ file size ≤ 
10
9
10 
9
 .
1
1 ≤ storage capacity per user ≤ 
10
9
10 
9
 .
Example:

Input:
["CloudStorage", "addUser", "addUser", "addFileBy", "compressFile", "compressFile", "compressFile", "compressFile", "getFileSize", "getFileSize", "copyFile", "addFileBy", "decompressFile", "updateCapacity", "decompressFile", "decompressFile", "decompressFile", "decompressFile"]

[[], ["user1", 1000], ["user2", 500], ["user1", "/dir/file.mp4", 500], ["user2", "/dir/file.mp4"], ["user3", "/dir/file.mp4"], ["user1", "/folder/non_existing_file"], ["user1", "/dir/file.mp4"], ["/dir/file.mp4.COMPRESSED"], ["/dir/file.mp4"], ["/dir/file.mp4.COMPRESSED", "/file.mp4.COMPRESSED"], ["user1", "/dir/file.mp4", 500], ["user1", "/dir/file.mp4.COMPRESSED"], ["user1", 2000], ["user2", "/dir/file.mp4.COMPRESSED"], ["user3", "/dir/file.mp4.COMPRESSED"], ["user1", "/dir/file.mp4.COMPRESSED"], ["user1", "/file.mp4.COMPRESSED"]]

Output:
[null, true, true, 500, -1, -1, -1, 750, 250, -1, true, 0, -1, 0, -1, -1, -1, 750]

Explanation:

CloudStorage();
addUser("user1", 1000); // Returns true.
addUser("user2", 500); // Returns true.
addFileBy("user1", "/dir/file.mp4", 500); // Returns 500.
compressFile("user2", "/dir/file.mp4"); // Returns -1; the file "/dir/file.mp4" is owned by "user1".
compressFile("user3", "/dir/file.mp4"); // Returns -1; "user3" doesn't exist
compressFile("user1", "/folder/non\_existing\_file"); // Returns -1; the file "/folder/non_existing_file" doesn't exist.
compressFile("user1", "/dir/file.mp4"); // Returns 750; the file "/dir/file.mp4" is compressed to size = 500 / 2 = 250 bytes.
getFileSize("/dir/file.mp4.COMPRESSED"); // Returns 250.
getFilesize("/dir/file.mp4");// Returns -1.
copyFile("/dir/file.mp4.COMPRESSED", "/file.mp4.COMPRESSED");// Returns true.
addFileBy("user1", "/dir/file.mp4", 500);// Returns 0.
decompressFile("user1", "/dir/file.mp4.COMPRESSED");// Returns true -1; "user1" does not have enough storage capacity to decompress the file.
updateCapacity("user1", 2000);// Returns 0.
decompressile("user2", "/dir/file.mp4.COMPRESSED");// Returns -1; the file "/dir/file.mp4.COMPRESSED" is owned by "user1".
decompressFile("user3", "/dir/file.mp4.COMPRESSED");// Returns -1; "user3" doesn't exist.
decompressFile("user1", "/dir/file.mp4.COMPRESSED");// Returns -1; the file "/dir/file.mp4" exists already.
decompressFile("user1", "/file.mp4.COMPRESSED");// Returns 750.

"""

"""
Implement a simplified version of an in-memory database to store records. Each record can be accessed with a unique identifier key of string type. A record may contain several field-value pairs, both of which are of string type.

Implement the InMemoryDB class:

void setData(String key, String field, String value) Should insert a field-value pair to the record associated with key.

If the field in the record already exists, replace the existing value with the specified value.
If the record does not exist, create a new one.
String getData(String key, String field) Should return the value contained within the field of the record associated with key.

If the record or the field doesn't exist, it should return "".
boolean deleteData(String key, String field) Should remove the field from the record associated with key.

Returns true if the field was successfully deleted, and false if the key or the field does not exist in the database.
Constraints:

Total number of calls to all methods ≤ 10⁵.
1 ≤ key.length, field.length, value.length ≤ 100.
All strings contain printable ASCII characters.
Example

Input:
["InMemoryDB", "setData", "setData", "getData", "getData", "deleteData", "deleteData"]
[[], ["A", "B", "E"], ["A", "C", "F"], ["A", "B"], ["A", "D"], ["A", "B"], ["A", "D"]]

Output:
[null, null, null, "E", "", true, false]

Explanation:

InMemoryDB db = new InMemoryDB();
db.setData("A", "B", "E"); // Returns null. Database state: {"A": {"B": "E"}}
db.setData("A", "C", "F"); // Returns null. Database state: {"A": {"C": "F", "B": "E"}}
db.getData("A", "B"); // Returns "E".
db.getData("A", "D"); // Returns "", since there is no value of field "D".
db.deleteData("A", "B"); // Returns true. Database state: {"A": {"C": "F"}}
db.deleteData("A", "D"); // Returns false. Database state: {"A": {"c": "F"}}


Follow-up 1:
The database should support displaying data based on filters. Introduce an operation to support printing some fields of a record.

Your task is to extend the existing InMemoryDB class with a new operation:

List<string> scanData(string key) Should return a list of strings representing the fields of a record associated with key.

The returned list should be in the following format ["<field1>(<value1>)", "<field2>(<value2>)", ...], where fields are sorted lexicographically.
If the specified record does not exist, return an empty list.
List<string> scanDataByPrefix(string key, string prefix) Should return a list of strings representing some fields of a record associated with key.

Specifically, only fields that start with prefix should be included.
The returned list should be in the same format as in the scanData operation, with fields sorted in lexicographical order.
Example:

Input:
["InMemoryDB", "setData", "setData", "setData", "scanDataByPrefix", "scanData", "scanDataByPrefix"]
[[], ["A", "BC", "E"], ["A", "BD", "F"], ["A", "C", "G"], ["A", "B"], ["A"], ["B", "B"]]

Output:
[null, null, null, null, ["BC(E)", "BD(F)"], ["BC(E)", "BD(F)", "C(G)"], []]

Explanation:

InMemoryDB db = new InMemoryDB();
db.setData("A", "BC", "E"); // Returns null. Database state: {"A": {"BC": "E"}}
db.setData("A", "BD", "F"); // Returns null. Database state: {"A": {"BC": "E", "BD": "F"}}
db.setData("A", "C", "G"); // Returns null. Database state: {"A": {"BC": "E", "BD": "F", "C": "G"}}
db.scanDataByPrefix("A", "B"); // Returns ["BC(E)", "BD(F)"].
db.scanData("A"); // Returns ["BC(E)", "BD(F)", "C(G)"].
db.scanDataByPrefix("B", "B"); // Returns [], since record "B" does not exist.


Follow-up 2:
Support the timeline of operations and TTL (Time-To-Live) settings for records and fields. Each operation from previous levels now has an alternative version with a timestamp parameter to represent when the operation was executed. For each field-value pair in the database, the TTL determines how long that value will persist before being removed.

Notes:

Time should always flow forward, so timestamps are guaranteed to strictly increase as operations are executed.

Each test cannot contain both versions of operations (with and without a timestamp). However, you should maintain backward compatibility, so all previously defined methods should work in the same way as before.

Your task is to extend the existing InMemoryDB class with a new operation:

void setDataAt(String key, String field, String value, int timestamp) Should insert a field-value pair or update the value of the field in the record associated with key.

void setDataAtWithTtl(String key, String field, String value, int timestamp, int ttl) Should insert a field-value pair or update the value of the field in the record associated with key.

Also sets its Time-To-Live starting at timestamp to be ttl.
The ttl is the amount of time that this field-value pair should exist in the database, meaning it will be available during this interval: [timestamp, timestamp + ttl).
boolean deleteDataAt(String key, String field, int timestamp) The same as deleteData, but with the timestamp of the operation specified.

Should return true if the field existed and was successfully deleted, and false if the key didn't exist.
String getDataAt(String key, String field, int timestamp) The same as getData, but with the timestamp of the operation specified.

List<String> scanDataAt(String key, int timestamp) The same as scanData, but with the timestamp of the operation specified.

List<String> scanDataByPrefixAt(String key, String prefix, int timestamp) The same as scanDataByPrefix, but with the timestamp of the operation specified.

Example 1:

Input:
["InMemoryDB", "setDataAtWithTtl", "setDataAtWithTtl", "setDataAt", "scanDataByPrefixAt", "scanDataByPrefixAt"]
[[], ["A", "BC", "E", 1, 9], ["A", "BC", "E", 5, 10], ["A", "BD", "F", 5], ["A", "", 14], ["A", "", 15]]

Output:
[null, null, null, null, ["BC(E)", "BD(F)"], ["BD(F)"]]

Explanation:

InMemoryDB db = new InMemoryDB();
db.setDataAtWithTtl("A", "BC", "E", 1, 9); // Returns null. Database state: {"A": {"BC": "E"}}, where {"BC": "E"} expires at timestamp 10
db.setDataAtWithTtl("A", "BC", "E", 5, 10); // Returns null. Database state: {"A": {"BC": "E"}}, as field "BC" in record "A" already exists, it was overwritten, and {"BC": "E"} now expires at timestamp 15.
db.setDataAt("A", "BD", "F", 5); // Returns null. Database state: {"A": {"BC": E", "BD": "F"}}, where {"BD": "F"} does not expire.
db.scanDataByPrefixAt("A", "", 14); // Returns ["BC(E)", "BD(F)"].
db.scanDataByPrefixAt("A", "", 15); // Returns ["BD(F)"].
Example 2:

Input:
["InMemoryDB", "setDataAt", "setDataAtWithTtl", "getDataAt", "setDataAtWithTtl", "scanDataAt", "scanDataAt", "scanDataAt", "deleteDataAt"]
[[], ["A", "B", "C", 1], ["X", "Y", "Z", 2, 15], ["X", "Y", 3], ["A", "D", "E", 4, 10], ["A", 13], ["X", 16], ["X", 17], ["X", "Y", 20]]

Output:
[null, null, null, "Z", null, ["B(C)", "D(E)"], ["Y(Z)"], [], false]

Explanation:

InMemoryDB db = new InMemoryDB();
db.setDataAt("A", "B", "C", 1); // Returns null. Database state: {"A": {"B": "C"}}.
db.setDataAtwithTtl("X", "Y", "Z", 2, 15); // Returns null. Database state: {"X": {"Y": "Z"}, "A": {"B": "C"}}, where {"Y": "z"} expires at timestamp 17.
db.getDataAt("X", "Y", 3); // Returns "Z".
db.setDataAtwithTtl("A", "D", "E", 4, 10); // Returns null. Database state: {"X": {"Y": "Z"}, "A": {"D": "E", "B": "C"}}, where {"D": "E"} expires at timestamp 14, and {"Y": "z"} expires at timestamp 17.
db.scanDataAt("A", 13); // Returns "B(C), D(E)".
db.scanDataAt("X", 16); // Returns "Y(Z)".
db.scanDataAt("X", 17);// Returns []. Note that all fields in record "X" have expired.
db.deleteDataAt("X", "Y", 20); // Returns false; The record "X" had expired at timestamp 17 and can't be deleted.


Follow-up 3:
The database should be backed up from time to time. Introduce operations to support backing up and restoring the database state based on timestamps. When restoring, ttl expiration times should be recalculated accordingly.

int backup(int timestamp) Should save the database state at the specified timestamp, including the remaining ttl for all records and fields.

Remaining ttl is the difference between their initial ttl and their current lifespan (the duration between the timestamp of this operation and their initial timestamp).
Returns the number of non-empty non-expired records in the database.
void restore(int timestamp, int timestampToRestore) Should restore the database from the latest backup before or at timestampToRestore.

It's guaranteed that a backup before or at timestampToRestore will exist.
Expiration times for restored records and fields should be recalculated according to the timestamp of this operation. Since the database timeline always flows forward, restored records and fields should expire after the timestamp of this operation, depending on their remaining ttls at backup.
Constraints:

Method calls ≤ 
10
5
10 
5
 
1 ≤ key.length, field.length, value.length ≤ 100
All strings contain printable ASCII characters.
timestamp values strictly increase in a single test case.
Example:

Input:
["InMemoryDB", "setAtWithTtl", "backup", "setDataAt", "backup", "deleteDataAt", "backup", "restore", "backup", "scanDataAt", "scanDataAt"]
[[], ["A", "B", "C", 1, 10], [3], ["A", "D", "E", 4], [5], ["A", "B", 8], [9], [10, 7], [11], ["A", 15], ["A", 16]]

Output:
[null, null, 1, null, 1, true, 1, null, 1, ["B(C)", "D(E)"], ["D(E)"]]

Explanation:

InMemoryDB db = new InMemoryDB();
db.setDataAtWithTtl("A", "B", "C", 1, 10); // Returns null, database state: {"A": {"B": "C"}} with lifespan [1, 11), meaning that the record should be deleted at timestamp 11.
db.backup(3); // Returns 1; Saves the database state.
db.setDataAt("A", "D", "E", 4); // Returns null; Database state: {"A": {"D": "E", "B": "C"}}
db.backup(5); // Returns 1. Saves the database state.
db.deleteDataAt("A", "B", 8); // Returns true; Database state: {"A": {"D": "E"}}
db.backup(9); //Returns 1; saves the database state
db.restore(10, 7); // Returns null; Restores the database to the state of last backup at timestamp 5: {"A": {"D": "E", "B": "C"}} with {"B": "C"} expiring at timestamp = 16; since the initial ttl of the field is 10 and the database was restored to the state at timestamp 5; this field has had a lifespan of 4 and a remaining ttl of 6, so it will now expire at timestamp = 10 + 6 = 16.
db.backup(11); // Returns 1; saves the database state
db.scanDataAt("A", 15); // Returns ["B(C)", "D(E)"]
db.scanDataAt("A", 16); // Returns ["D(E)"]

"""

"""
Design a simple banking system that supports creating customer accounts, depositing money, and transferring funds between accounts. Each operation is timestamped with increasing integer times to simulate a real-time system.

Implement the BankingSystem class:

BankingSystem() Initializes the banking system with no accounts.

boolean createAccount(int timestamp, String accountId) Creates a new account identified by accountId with a zero balance.

Returns true if the account is created successfully.
Returns false if an account with the same accountId already exists.
int deposit(int timestamp, String accountId, int amount) Adds amount to the balance of the existing account accountId.

Returns the new balance if the account exists.
Returns -1 if accountId does not exist.
int transfer(int timestamp, String sourceAccountId, String targetAccountId, int amount) Transfers amount from sourceAccountId to targetAccountId.

Returns the new balance of sourceAccountId if the transfer succeeds.
Returns -1 if either account does not exist, the IDs are the same, or sourceAccountId has insufficient funds.
Example

Input:
["BankingSystem", "createAccount", "createAccount", "createAccount", "deposit", "deposit", "transfer", "transfer"]

[[], [1, "account1"], [2, "account1"], [3, "account2"], [4, "non-existing", 2700], [5, "account1", 2700], [6, "account1", "account2", 2701], [7, "account1", "account2", 200]]

Output:
[null, true, false, true, -1, 2700, -1, 2500]

Explanation:

BankingSystem bs = new BankingSystem();
bs.createAccount(1, "account1"); // Returns true.
bs.createAccount(2, "account1"); // Returns false. Account "account1" already exists.
bs.createAccount(3, "account2"); // Returns true.
bs.deposit(4, "non-existing", 2700); // Returns -1. The account does not exist.
bs.deposit(5, "account1", 2700); // Returns 2700.
bs.transfer(6, "account1", "account2", 2701); // Returns -1. Insufficient funds in "account1".
bs.transfer(7, "account1", "account2", 200); // Returns 2500. It's the new balance of "account1" after transferring $200.

Follow-up 1:
Extend the existing BankingSystem class with a new operation:

List<String> topSpenders(int timestamp, int n) Returns the top n accounts ranked by their total outgoing transactions, which is defined as the sum of all money transferred out or withdrawn. Return the result as a list of strings in the format ["<accountId1>(<totalOutgoing1>)", "<accountId2>(<totalOutgoing2>)", ...], sorted by:

Total outgoing amount in descending order.
Account ID in ascending lexicographical order to break ties.
If there are fewer than n accounts, include all accounts in the result. Accounts with a total outgoing sum of zero should also be included (displayed as "(0)"), and should be sorted alphabetically if there is a tie at zero.

Example

Input:
["BankingSystem", "createAccount", "createAccount", "createAccount", "deposit", "deposit", "deposit", "topSenders", "transfer", "transfer", "transfer", "topSenders"]

[[], [1, "account3"], [2, "account2"], [3, "account1"], [4, "account2", 2000], [5, "account3", 3000], [6, "account1", 4000], [7, 3], [8, "account3", "account2", 500], [9, "account3", "account1", 1000], [10, "account1", "account2", 2500], [11, 3]]

Output:
[null, true, true, true, 2000, 3000, 4000, ["account1(0)", "account2(0)", "account3(0)"], 3500, 2500, 500, ["account2(1500)", "account3(500)", "account1(0)"]]

Explanation:

BankingSystem bs = new BankingSystem();
bs.createAccount(1, "account3"); // Returns true.
bs.createAccount(2, "account2"); // Returns true.
bs.createAccount(3, "account1"); // Returns true.
bs.deposit(4, "account2", 2000); // Returns 2000.
bs.deposit(5, "account3", 3000); // Returns 3000.
bs.deposit(6, "account1", 4000); // Returns 4000.
bs.topSpenders(7, 3); // Returns ["account1(0)", "account2(0)", "account3(0)"]. None of the accounts has any outgoing transactions, so they are sorted alphabetically.
bs.transfer(8, "account3", "account2", 500); // Returns 3500. "account3" balance becomes $3500; outgoing total becomes $500.
bs.transfer(9, "account3", "account1", 1000); // Returns 2500. "account3" balance becomes $2500; outgoing total becomes $1500.
bs.transfer(10, "account1", "account2", 2500); // Returns 500. "account1" balance becomes $500; outgoing total becomes $2500.
bs.topSpenders(11, 3); // Returns ["account1(2500)", "account3(1500)", "account2(0)"]. Sorted by total outgoing in descending order.



"""



"""
Given a list of stock transactions ordered by timestamp. Each transaction is either a "buy" or a "sell" and is represented as a list of strings in the format of: [<timestamp>, <type>, <amount>, <price>]. Each sell transaction incurs a 10% tax on the profit earned. If no profit is made, the tax is zero.

Assume a person follows a strategy of selling the highest-cost stock first to avoid tax when possible. Calculate the total tax on all sales.

Constraints:

Transactions are sorted by timestamp in ascending order.
timestamp, amount, and price are integers in string format.
All sell transactions have sufficient stock from previous buy transactions.
1 <= transactions.length <= 
10
5
10 
5
 
1 <= amount <= 
10
5
10 
5
 
1 <= price <= 
10
5
10 
5
 
Example 1:

Input:  transactions = [["1","buy","100","20"], ["2","buy","50","30"], ["3","sell","80","25"], ["4","sell","60","35"]]
Output: 105.0
Explanation: According to the rules, the following steps are taken during the sell operations:

Sell 80 units at $25:
Sell 50 units bought at $30: Profit per unit = $25 - $30 = -$5 (no tax).
Sell remaining 30 units bought at $20: Profit per unit = $25 - $20 = $5.
Total profit from this sale = 30 * $5 = $150.
Tax = 10% of $150 = $15.
Sell 60 units at $35:
Sell 60 units bought at $20: Profit per unit = $35 - $20 = $15.
Total profit from this sale = 60 * $15 = $900.
Tax = 10% of $900 = $90.
Total Tax Paid: $15 + $90 = $105.
Example 2:

Input: transactions = [["1","buy","20","50"], ["2","sell","10","60"], ["3","buy","15","55"], ["4","sell","10","65"], ["5","sell","10","70"]]
Output: 37.5

Example 3:

Input: transactions = [["1","buy","10","10"], ["2","buy","20","20"], ["3","buy","30","105"], ["4","sell","10","100"], ["5","sell","20","120"], ["6","sell","30","50"]]
Output: 130.0
"""


"""

You are provided with a JSON configuration containing various traits (e.g., "nose", "mouth", "eyes") and their respective possible values. You are asked to randomly generate n random Non-fungible tokens (NFTs) based on these traits. Each NFT must select exactly one value for every trait. In this scenario, duplicates are permitted, meaning multiple generated NFTs can have the same combination of traits.

Example JSON Configuration:

{
    "name": "config-1",
    "size": "large",
    "traits": {
        "nose": ["pointy", "tiny", "flat"],
        "mouth": ["small", "wide", "thin"],
        "eyes": ["blue", "green", "brown"]
    },
    ...
}
Constraints:

You can assume the JSON string is valid and includes a traits field.
The number of traits can vary, and each trait can have one or more possible values.
n can be any positive integer.
Example:

Input:
config = {
  "name": "config-1",
  "size": "large",
  "traits": {
    "nose": ["pointy", "tiny", "flat"],
    "mouth": ["small", "wide", "thin"],
    "eyes": ["blue", "green", "brown"]
  }
},
n = 5

Output:
[
  {"nose":"pointy","mouth":"small","eyes":"blue"},
  {"nose":"tiny","mouth":"wide","eyes":"green"},
  {"nose":"flat","mouth":"thin","eyes":"brown"},
  {"nose":"pointy","mouth":"small","eyes":"green"},
  {"nose":"tiny","mouth":"thin","eyes":"blue"}
]

Explanation: The above output contains 5 possible NFTs generated randomly using the provided traits. Each NFT is created by selecting one value at random for each trait.


Follow-up 1:
Keep all assumptions from the previous section, but now you are asked to generate n unique NFTs, ensuring that no two NFTs share the same combination of traits. If it is not possible to generate the specified number of unique NFTs based on the given n and configuration, an exception should be thrown.

Constraints:

You can assume the JSON string is valid and includes a traits field.
The number of traits can vary, and each trait can have one or more possible values.
n can be any positive integer.
No duplicate NFT combinations are allowed in the output.
Example 1:

Input:
config = {
  "name": "config-1",
  "size": "large",
  "traits": {
    "nose": ["pointy", "tiny", "flat"],
    "mouth": ["small", "wide", "thin"],
    "eyes": ["blue", "green", "brown"]
  }
},
n = 5

Output:
[
  {"nose":"pointy","mouth":"small","eyes":"blue"},
  {"nose":"tiny","mouth":"wide","eyes":"green"},
  {"nose":"flat","mouth":"thin","eyes":"brown"},
  {"nose":"pointy","mouth":"small","eyes":"green"},
  {"nose":"tiny","mouth":"thin","eyes":"blue"},
]

Explanation: The above output contains 5 possible NFTs generated randomly using the provided traits. Each NFT's traits combination is unique.

Example 2:

Input:
config = {
  "name": "simple",
  "size": "small",
  "traits": {
    "color": ["red", "blue", "green"],
    "shape": ["circle", "square"]
  }
},
n = 10

Output: An exception was thrown to indicate that n is too large for unique combinations

Explanation: From the given traits, we can generate at most 3 × 2 = 6 unique combinations.

Follow-up 2:
(This part is a variation of the LeetCode question 528. Random Pick with Weight. If you haven't completed that question yet, it is recommended to solve it first.)

To represent the rarity of certain traits, the configuration now includes a weight for each trait value. The weight determines the likelihood of selecting a specific trait value. The probability of picking a particular value is calculated as: probability = weight / (sum of all weights for the trait) , where the "sum of all weights" is the total weight of all possible values for the current trait.

For example:

{
  ...
  "traits": {
    "nose": [
      { "name": "pointy", "weight": 1 },
      { "name": "tiny", "weight": 2 },
      { "name": "flat", "weight": 3 }
    ],
    ...
  }
}
For the trait "nose", the probabilities of each value being generated are:

"pointy": 1 / (1 + 2 + 3) = 0.167 (16.7%)
"tiny": 2 / (1 + 2 + 3) = 0.333 (33.3%)
"flat": 3 / (1 + 2 + 3) = 0.5 (50%)
You are asked to generate n unique NFTs, ensuring that no two NFTs have identical combinations of traits. If it is not possible to generate the specified number of unique NFTs with the given configuration, an exception should be thrown.

Constraints:

Each trait’s weight is an integer in the range [1, 1000].
No duplicate NFT combinations are allowed in the output.
Example:

Input:
config = {
  "name": "config-1",
  "size": "large",
  "traits": {
    "nose": [
      {"name": "pointy", "weight": 1},
      {"name": "tiny", "weight": 2},
      {"name": "flat", "weight": 3}
    ],
    "mouth": [
      {"name": "small", "weight": 1000},
      {"name": "wide", "weight": 1},
      {"name": "thin", "weight": 1}
    ],
    "eyes": [
      {"name": "blue", "weight": 10},
      {"name": "green", "weight": 2},
      {"name": "brown", "weight": 1}
    ]
  }
},
n = 5

Output:
[
  {"nose": "pointy", "mouth": "small", "eyes": "blue"},
  {"nose": "tiny", "mouth": "small", "eyes": "brown"},
  {"nose": "tiny", "mouth": "small", "eyes": "green"},
  {"nose": "flat", "mouth": "small", "eyes": "blue"},
  {"nose": "tiny", "mouth": "small", "eyes": "blue"}
]

Explanation: The above output contains 5 possible NFTs generated randomly, and each NFT's trait combination is unique. The "mouth" trait with value "small" has a much larger weight, making it appear more frequently than "wide" or "thin".
"""

"""
Design a crypto trading system to manage cryptocurrency orders, supporting operations such as placing, pausing, resuming, canceling, and displaying live orders. Each order includes the following attributes:

ID: The current order ID.
Currency: The cryptocurrency being traded.
Amount: The amount of cryptocurrency in the order.
Timestamp: The time the order was placed.
Order Type: Either buy or sell.
State: One of live, paused, completed, or canceled.
Implement theCryptoTradingSystem class:

CryptoTradingSystem() Initialize the trading system.
String placeOrder(String id, String currency, int amount, int timestamp, String type) Place a new order with live status. Returns the order ID if successful, otherwise an empty string.
String pauseOrder(String id) Pause an live order. Returns the order ID if successful, otherwise an empty string.
String resumeOrder(String id) Resume a paused order. Returns the order ID if successful, otherwise an empty string.
String cancelOrder(String id) Cancel an existing order that is either live or paused. Returns the order ID if successful, otherwise an empty string.
String completeOrder(String id) Complete an live order. Returns the order ID if successful, otherwise an empty string.
List<String> displayLiveOrders() Display all live orders, sorted by ascending timestamp.
Constraints:

Order IDs are unique strings.
The system should handle multiple orders efficiently.
Operations should maintain the correct state transitions for each order.
Example:

Input:
["CryptoTradingSystem","placeOrder","placeOrder","placeOrder","pauseOrder","displayLiveOrders","resumeOrder","resumeOrder","cancelOrder","completeOrder","completeOrder","displayLiveOrders"]

[[],["order-1","BTC",100,1,"buy"],["order-2","ETH",50,2,"sell"],["order-3","BNB",30,3,"buy"],["order-1"],[],["order-1"],["order-2"],["order-2"],["order-3"],["order-3"],[]]

Output:
[null,"order-1","order-2","order-3","order-1",["order-2","order-3"],"order-1","", "order-2","order-3","",["order-1"]]

Explanation:

CryptoTradingSystem system = new CryptoTradingSystem()
system.placeOrder("order-1","BTC",100,1,"buy"); // Return "order-1".
system.placeOrder("order-2","ETH",50,2,"sell"); // Return "order-2".
system.placeOrder("order-3","BNB",30,3,"buy"); // Return "order-3".
system.pauseOrder("order-1"); // Return "order-1".
system.displayLiveOrders(); // Return ["order-2","order-3"] as "order-1" is paused.
system.resumeOrder("order-1"); // Return "order-1".
system.resumeOrder("order-2"); // Return "" as "order-2" is not paused.
system.cancelOrder("order-2"); // Return "order-2".
system.completeOrder("order-3") // Return "order-3".
system.completeOrder("order-3") // Return "" as "order-3" was completed before.
system.displayLiveOrders()// Return ["order-1"] as "order-1" is the only live order ("order-2" is canceled and "order-3" is completed).


Follow-up 1:
Now we want the system to manage orders for multiple users. To achieve this, we've introduced an additional field userId for placing orders. Additionally, we want to support the functionality to cancel all orders associated with a specific user.

Each order now includes the following attributes:

ID: The current order ID.
Currency: The cryptocurrency being traded.
Amount: The amount of cryptocurrency in the order.
Timestamp: The time the order was placed.
Order Type: Either buy or sell.
State: One of live, paused, completed, or canceled.
(New) User ID: The user of the current order belongs to.
Extend your solution and implement CryptoTradingSystem class:

CryptoTradingSystem() Initialize the trading system.
(New) String placeOrder(String id, String currency, int amount, int timestamp, String type, String userId) Place a new order with live status for the given user.
String pauseOrder(String id) Pause an live order.
String resumeOrder(String id) Resume a paused order.
String cancelOrder(String id) Cancel an existing order that is either live or paused.
String completeOrder(String id) Complete an live order.
List<String> displayLiveOrders() Display all live orders, sorted by ascending timestamp.
(New) int cancelAllOrders(String userId): Cancel all orders associated with a given userId. Return the number of orders successfully canceled.
Example:

Input:
["CryptoTradingSystem","placeOrder","placeOrder","placeOrder","pauseOrder","displayLiveOrders","resumeOrder","resumeOrder","cancelOrder","completeOrder","completeOrder","displayLiveOrders","cancelAllOrders","displayLiveOrders"]

[[],["order-1","BTC",100,1,"buy"],["order-2","ETH",50,2,"sell"],["order-3","BNB",30,3,"buy"],["order-1"],[],["order-1"],["order-2"],["order-2"],["order-3"],["order-3"],[],["user-1"],[]]

Output:
[null,"order-1","order-2","order-3","order-1",["order-2","order-3"],"order-1","", "order-2","order-3","",["order-1"],1,[]]

Explanation:

CryptoTradingSystem system = new CryptoTradingSystem()
system.placeOrder("order-1","BTC",100,1,"buy","user-1"); // Return "order-1".
system.placeOrder("order-2","ETH",50,2,"sell","user-2"); // Return "order-2".
system.placeOrder("order-3","BNB",30,3,"buy","user-2"); // Return "order-3".
system.pauseOrder("order-1"); // Return "order-1".
system.displayLiveOrders(); // Return ["order-2","order-3"].
system.resumeOrder("order-1"); // Return "order-1".
system.resumeOrder("order-2"); // Return "".
system.cancelOrder("order-2"); // Return "order-2".
system.completeOrder("order-3"); // Return "order-3".
system.completeOrder("order-3"); // Return "".
system.displayLiveOrders();// Return ["order-1"].
system.cancelAllOrders("user-1");// Return 1 as user "user-1" only has one order can be canceled.
system.displayLiveOrders();// Return [].

Follow-up 2:
As the number of users in the trading system continues to grow, handling all orders in a single data stream is no longer feasible. To address this, the data needs to be partitioned into n separate streams. All orders belonging to the same user must remain within the same stream. Implement the following methods while maintaining the functionality from the previous section.

Extend your solution and implement CryptoTradingSystem class:

(New) CryptoTradingSystem(int n) Initialize the trading system with the given number of data streams.
String placeOrder(String id, String currency, int amount, int timestamp, String type, String userId) Place a new order with live status for the given user.
String pauseOrder(String id) Pause an live order.
String resumeOrder(String id) Resume a paused order.
String cancelOrder(String id) Cancel an existing order that is either live or paused.
String completeOrder(String id) Complete an live order.
List<String> displayLiveOrders() Display all live orders, sorted by ascending timestamp.
int cancelAllOrders(String userId): Cancel all orders associated with a given userId.
Example:

Input:
["CryptoTradingSystem","placeOrder","placeOrder","placeOrder","pauseOrder","displayLiveOrders","resumeOrder","resumeOrder","cancelOrder","completeOrder","completeOrder","displayLiveOrders","cancelAllOrders","displayLiveOrders"]

[[3],["order-1","BTC",100,1,"buy"],["order-2","ETH",50,2,"sell"],["order-3","BNB",30,3,"buy"],["order-1"],[],["order-1"],["order-2"],["order-2"],["order-3"],["order-3"],[],["user-1"],[]]

Output:
[null,"order-1","order-2","order-3","order-1",["order-2","order-3"],"order-1","", "order-2","order-3","",["order-1"],1,[]]

Explanation:
For all operations, the output should be the same as the previous part.
"""

"""
Design a custom iterator that filters elements from a provided list based on a specified filter function 
F
(
n
)
F(n). The iterator should return only the elements that satisfy the filter condition (considered "valid") while preserving their original order.

Note that the dataset may contain over a million elements, but the number of next() calls is relatively small, the implementation must be efficient and optimized for this use case.

Implement the FilteringIterator class:

FilteringIterator(List<Integer> arr, Predicate<Integer> filter): Initializes the iterator with a list of integers and a filter function.
boolean hasNext(): Returns true if there are additional valid elements remaining in the sequence to iterate over.
int next(): Returns the next valid integer in the sequence.
Constraints:

The list contains between 0 and 105 elements.
Each element in the list is an integer within the range [-109, 109].
The filter function can perform any valid integer-based condition.
Example 1:

Input: nums = [1, 2, 3, 4, 5, 6, 7, 8], 
F
(
n
)
F(n) = n -> n % 2 == 0
Output: [2, 4, 6, 8]
Explanation: The filter function filters out even numbers from the array. By calling next() repeatedly until hasNext() returns false, the order of elements returned by next should be: [2, 4, 6, 8]

Example 2:

Input: nums = [0, 3, 5, 7, 10, 12, 15], 
F
(
n
)
F(n) = n -> n > 5
Output: [7, 10, 12, 15]

Example 3:

Input: nums = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], filter = x -> isPrime(x)
Output: [2, 5, 7, 11, 13]
"""

"""
(This question is a variation of the LeetCode question 281. Zigzag Iterator. If you haven't completed that question yet, it is recommended to solve it first.)

Create an interleaving iterator for a list of integer arrays, which alternates between arrays in a round-robin manner. The behavior of the iterator depends on a boolean flag indicating whether it should cycle through the arrays:

Non-cycled behavior: The iterator returns elements in an interleaved order until all elements from all arrays are exhausted.
Cycled behavior: After exhausting all elements, the iterator restarts from the beginning, ensuring that hasNext() always returns true.
Implement the InterleaveIterator class:

InterleaveIterator(int[][] arr, boolean isCycled) Initializes the iterator with a 2D integer array and a flag to determine whether the iterator cycles.
boolean hasNext() Returns true if there are elements remaining in the non-cycled mode or always returns true in the cycled mode.
int next() Retrieves the next element from the iterator in the interleaved order. In the cycled mode, it continues to loop through the arrays indefinitely.
Constraints:

1 <= number of sub-arrays <= 
10
5
10 
5
 
The sum of lengths across all sub-arrays <= 
10
5
10 
5
 
Each element fits within a 32-bit integer
Example 1:

Input: arr = [[1, 2], [3], [4]], isCycled = true, next() called 10 times
Output: [1, 3, 4, 2, 1, 3, 4, 2, 1, 3]
Explanation: By calling next() 10 times repeatedly, the order of elements returned by next should be [1, 3, 4, 2, 1, 3, 4, 2, 1, 3]. Here's the breakdown of all steps:

iterator.next(); // Return 1, the first element from the first array, remains: [[2], [3], [4]]
iterator.next(); // Return 3, the first element from the second array, remains: [[2], [], [4]]
iterator.next(); // Return 4, the first element from the third array, remains: [[2], [], []]
iterator.next(); // Return 2, the only element from the first array, remains: [[], [], []]
iterator.next(); // Return 1, since cycling is enabled, restarts iteration and returns the first element from the first array again, remains: [[2], [3], [4]]]
iterator.next(); // Return 3.
iterator.next(); // Return 4.
iterator.next(); // Return 2.
iterator.next(); // Return 1. Restarts the iteration again.
iterator.next(); // Return 3.
Example 2:

Input: arr = [[1, 2], [3, 4], [5, 6]], isCycled = false, next() repeatedly until hasNext() returns false
Output: [1, 3, 5, 2, 4, 6]

Example 3:

Input: arr = [[1, 2], [3], [4, 5, 6, 7]], isCycled = true, next() called 12 times
Output: [1, 3, 4, 2, 5, 6, 7, 1, 3, 4, 2, 5]
"""