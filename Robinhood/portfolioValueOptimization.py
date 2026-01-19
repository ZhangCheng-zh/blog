"""
Portfolio Value Optimization
You have some securities available to buy that each has a price Pi.
Your friend predicts for each security the stock price will be Si at some future date.
But based on volatility of each share, you only want to buy up to Ai shares of each security i.
Given M dollars to spend, calculate the maximum value you could potentially
achieve based on the predicted prices Si (and including any cash you have remaining).

Pi = Current Price
Si = Expected Future Price
Ai = Maximum units you are willing to purchase
M = Dollars available to invest
Example 1:
Input:
M = $140 available
N = 4 Securities
P1=15, S1=45, A1=3 (AAPL)
P2=40, S2=50, A2=3 (BYND)
P3=25, S3=35, A3=3 (SNAP)
P4=30, S4=25, A4=4 (TSLA)

Output: $265 (no cash remaining) 
3 shares of apple -> 45(15 *3), 135(45 *3)
3 shares of snap -> 75, 105
0.5 share of bynd -> 20, 25
"""
def maxPortfolioValue(M, sec):
    deals = []
    for symbol, p, s, a in sec:
        p = float(p)
        s = float(s)
        a = float(a)
        if s > p:
            deals.append((s / p, p, s, a))
    
    deals.sort(reverse = True, key = lambda x: x[0])

    cash = float(M)
    future = cash

    for _, p, s, a in deals:
        if cash <= 0:
            break

        spend = min(cash, p * a)
        shares = spend / p 

        cash -= spend
        future += shares * (s - p)

    return future # time: O(nlgn) space: O(n)


# T1: sample 1 (mix full + fractional buy, skip losing stock)
M = 140
sec = [
    ["AAPL", "15", "45", "3"],
    ["BYND", "40", "50", "3"],
    ["SNAP", "25", "35", "3"],
    ["TSLA", "30", "25", "4"],
]
# buy 3 AAPL (cost 45, future 135), 3 SNAP (cost 75, future 105), 0.5 BYND (cost 20, future 25)
expected = 265.0
assert maxPortfolioValue(M, sec) == expected


# T2: sample 2 (no profitable trades -> keep all cash)
M = 100
sec = [
    ["AAPL", "15", "10", "3"],
    ["BYND", "40", "35", "3"],
]
expected = 100.0
assert maxPortfolioValue(M, sec) == expected


# T3: sample 3 (best ROI first, then remainder cash)
M = 50
sec = [
    ["SNAP", "20", "30", "5"],  # ROI=1.5
    ["AAPL", "50", "70", "2"],  # ROI=1.4
]
# buy 2.5 SNAP (spend 50) -> future 2.5*30 = 75
expected = 75.0
assert maxPortfolioValue(M, sec) == expected


# T4: fractional across a cap (can't exceed Ai)
M = 100
sec = [
    ["X", "10", "20", "3"],   # can spend at most 30
    ["Y", "10", "15", "100"], # spend rest here
]
# buy 3 X -> spend 30, future 60
# remaining 70 -> buy 7 Y -> future 105
expected = 165.0
assert maxPortfolioValue(M, sec) == expected


# T5: exact budget not required (leftover cash kept)
M = 7
sec = [
    ["A", "5", "6", "1"],  # spend at most 5, profit small
]
# buy 1 share: spend 5, future value = 6 + leftover cash 2 = 8
expected = 8.0
assert maxPortfolioValue(M, sec) == expected


# T6: tie ROI (either order yields same future value)
M = 10
sec = [
    ["A", "2", "4", "2"],  # ROI=2, max spend 4
    ["B", "3", "6", "2"],  # ROI=2, max spend 6
]
# spend all 10 at ROI 2 => future 20
expected = 20.0
assert maxPortfolioValue(M, sec) == expected
