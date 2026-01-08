"""
Codewriting

Overview:

Our goal is to build a simplified version of a real Robinhood system that reads prices from a stream and aggregates those prices into historical datapoints aka candlestick charts. We’re looking for clean code, good naming, testing, etc.

Step 1: Parse Prices

Your input will be a comma-separated string of prices and timestamps in the format price:timestamp e.g.

1:0,3:10,2:12,4:19,5:35 is equivalent to

price: 1, timestamp: 0
price: 3, timestamp: 10
price: 2, timestamp: 12
price: 4, timestamp: 19
price: 5, timestamp: 35

You can assume the input is sorted by timestamp and values are non-negative integers.

Step 2: Aggregate Historical Data from Prices

We calculate historical data across fixed time intervals. In this case, we’re interested in intervals of 10, so the first interval will be [0, 10). For each interval, you’ll build a datapoint with the following values.

Start time
First price
Last price
Max price
Min price

Important: If an interval has no prices, use the previous datapoint’s last price for all prices. If there are no prices and no previous datapoints, skip the interval.

You should return a string formatted as {start,first,last,max,min}. For the prices shown above, the expected datapoints are

{0,1,1,1,1}{10,3,4,4,2}{20,4,4,4,4}{30,5,5,5,5}

[execution time limit] 3 seconds (cs)

[input] string prices_to_parse

[output] string

[C#] Syntax Tips

// Prints help message to the console
// Returns a string
string helloWorld(string name) {
Console.Write("This prints to the console when you Run Tests");
return "Hello, " + name;
}

C#
Mono v6.12.0.122
14151611121391067845
}
else
{
if (i > 0 && list[i-1] != null)
{
AggregatePrice aggPrice = new AggregatePrice(list[i-1].lastPrice, i10);
str.Append("{");
str.Append(GetAggregatedPrice(i10, aggPrice));
str.Append("}");
}

TESTS
CUSTOM TESTS
RESULTS
Tests passed: 0/3. Compilation error.
Test 1
Input:
prices_to_parse: "1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8,10:9,11:10,12:11,13:12,14:13,15:14,16:15,17:16,18:17,19:18,20:19"
Output:
undefined
Expected Output:
"{0,1,10,10,1}{10,11,20,20,11}"
Console Output:
Empty
Test 2
Test 3

Overview
You are building an application that consists of many different services that can depend on each other. One of these services is the entrypoint which receives user requests and then makes requests to each of its dependencies, which will in turn call each of their dependencies and so on before returning.
Given a directed acyclic graph that contains these dependencies, you are tasked with determining the "load factor" for each of these services to handle this load. The load factor of a service is defined as the number of units of load it will receive if the entrypoint receives a 1 unit of load. Note that we are interested in the worst case capacity. For a given downstream service, its load factor is the number of units of load it is required to handle if all upstream services made simultaneous requests. For example, in the following dependency graph where A is the entrypoint:

Each query to A will generate one query to B which will pass it on to C and from there to D. A will also generate a query to C which will pass it on to D, so the worst case (maximum) load factors for each service is A:1, B:1, C:2, D:2.
(Important: make sure you've fully understood the above example before proceeding!)

Problem Details

service_list: An array of strings of format service_name=dependency1,dependency2. Dependencies can be blank (e.g. dashboard=) and non-existent dependency references should be ignored (e.g. prices=users,foobar and foobar is not a service defined in the graph). Each service is defined only once in the graph.
entrypoint: An arbitrary service that is guaranteed to exist within the graph
Output: A list of all services depended by (and including) entrypoint as an array of strings with the format service_name*load_factor sorted by service name.
Example

Input:
service_list = ["logging=",
"user=logging",
"orders=user,foobar",
"recommendations=user,orders",
"dashboard=user,orders,recommendations"]
entrypoint = "dashboard"

Output (note sorted by service name)
["dashboard1",
"logging4",
"orders2",
"recommendations1",
"user*4"]
[execution time limit] 3 seconds (cs)

[input] array.string service_list

[input] string entrypoint

[output] array.string

[C#] Syntax Tips

// Prints help message to the console
// Returns a string
string helloWorld(string name) {
Console.Write("This prints to the console when you Run Tests");
return "Hello, " + name;
}
"""