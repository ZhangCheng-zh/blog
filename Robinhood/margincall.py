"""
## Customer Portfolio From Trade Stream (with Follow-ups)
You are given a customer’s trade records in timestamp order.
Each trade is a list of strings:

`[timestamp, symbol, side, quantity, price]`

* `side` is `"B"` (buy) or `"S"` (sell)
* `quantity` and `price` are non-negative integers (as strings)
* The customer starts with **cash = 1000** and **0 shares** of every stock.

Return the final portfolio as a list of `[symbol, quantity]` strings:
* Include `["CASH", <cash>]`
* Include only stocks with quantity > 0
* Sort stock symbols alphabetically (CASH can be first)
---

# Follow-up 0 (Base) — Build Portfolio (Tests 1–4)
Process trades in order:

* **Buy**:
  `cash -= quantity * price`
  `shares[symbol] += quantity`

* **Sell**:
  `cash += quantity * price`
  `shares[symbol] -= quantity`
  (Trades are valid: you never sell more than you own.)

Output final portfolio.

---
# Follow-up 2 — Collateral Constraint (Tests 8–10)
Some symbols are **special**: symbols ending with `"O"` (letter O).
For a special stock like `"AAPLO"`, its **collateral stock** is `"AAPL"` (remove the trailing `"O"`).

Constraint (must always hold):
* At all times:
  `shares[collateral] >= shares[special]`

During margin calls:
* You can only sell **non-collateral** shares.
* A collateral stock share is **not sellable** if selling it would break the constraint.
* Special stocks **can be sold**, and selling special shares may free collateral shares to become sellable later.

---

### Notes / Assumptions
* Input is sorted by timestamp.
* All numeric fields are non-negative integers (as strings).
* In base version, trades keep cash non-negative.
* In follow-ups, the margin call rules ensure the process can restore cash to non-negative.

If you want, I can also provide the clean Python solution starting from base → add margin call → add collateral step-by-step.
"""


"""
# Follow-up 1 — Margin Call (Tests 5–7)
Now buys may cause cash to become negative.
After processing a **buy**, if `cash < 0`, perform a **margin call**:

* Force-sell shares from the customer’s portfolio until `cash >= 0`
* You may sell any number of shares of a symbol at its **most recently traded price**
* Sell priority:
  1. Higher most-recent price first
  2. If tie, alphabetically smaller symbol first
* Selling one share adds `price` to cash and decreases shares by 1.
* Margin call may sell shares of the stock that was just bought.
""" 

"""
Follow-up 2 — Collateral Constraint
Special stocks end with "O" (letter O). Example: "AAPLO" is special, collateral is "AAPL".

Constraint must always hold:
shares[collateral] >= shares[special]

During margin call:
You may only sell non-collateral shares
A collateral share is sellable only if it won’t break the constraint
Selling special shares can free collateral shares
"""


import math
from collections import defaultdict

def formatPortfolio(cash, shares):
    result = [['CASH', str(cash)]]
    for symbol in sorted(shares.keys()):
        if shares[symbol] > 0:
            result.append([symbol, str(shares[symbol])])
    return result

def isSpecial(symbol):
    return symbol.endswith('O')

def getSellableShares(symbol, shares, followUp):
    have = shares[symbol]
    if have <= 0:
        return 0
    
    if followUp <= 1: # everything sellable in follow-up 1
        return have
    
    if isSpecial(symbol):
        return have 

    special = symbol + 'O'
    locked = shares[special] # must keep no less than special symbol count

    return max(0, have - locked)

def pickBestSellableSymbol(shares, lastPrice, followUp, soldSpecial):
    bestSymbol = None
    bestPrice = -1

    for symbol in list(shares.keys()):
        if followUp == 2 and symbol in soldSpecial:
            continue
        if getSellableShares(symbol, shares, followUp) <= 0:
            continue

        price = lastPrice[symbol]

        if price > bestPrice or (price == bestPrice and (bestSymbol is None or symbol < bestSymbol)):
            bestPrice = price
            bestSymbol = symbol
    
    return bestSymbol



def runMarginCall(cash, shares, lastPrice, followUp):
    soldSpecial = set()

    while cash < 0:
        bestSymbol = pickBestSellableSymbol(shares, lastPrice, followUp, soldSpecial)
        price = lastPrice[bestSymbol]

        needShares = math.ceil((-cash) / price)
        canSell = getSellableShares(bestSymbol, shares, followUp)
        sellQty = min(needShares, canSell)

        shares[bestSymbol] -= sellQty
        cash += sellQty * price

        if followUp == 2 and isSpecial(bestSymbol):
            soldSpecial.add(bestSymbol)

        if shares[bestSymbol] == 0:
            del shares[bestSymbol]
    
    return cash

def buildPortfolio(trades, followUp):
    # followup 0 base only
    # followup 1 margin call(no collateral)
    # followup 2 margin call + collateral
    cash = 1000
    shares = defaultdict(int)
    lastPrice = {}

    for _,symbol, side, qtyStr, priceStr in trades:
        qty = int(qtyStr)
        price = int(priceStr)
        lastPrice[symbol] = price

        if side == 'B':
            cash -= qty * price
            shares[symbol] += qty

            if followUp >= 1 and cash < 0:
                cash = runMarginCall(cash, shares, lastPrice, followUp)
        else:
            cash += qty * price
            shares[symbol] -= qty
            if shares[symbol] == 0:
                del shares[symbol]
    
    return formatPortfolio(cash, shares)


# =========================
# Test cases for Follow-up 0 / 1 / 2
# Assumes you have:
#   buildPortfolio(trades, followUp)
# where followUp in {0,1,2}
# =========================

# ---------- Follow-up 0 (Base only) ----------
# T0-1: sample 1
trades = [
    ["1", "AAPL", "B", "10", "10"],
    ["3", "GOOG", "B", "20", "5"],
    ["10", "AAPL", "S", "5", "15"],
]
expected = [["CASH", "875"], ["AAPL", "5"], ["GOOG", "20"]]
assert buildPortfolio(trades, 0) == expected

# T0-2: sell all shares -> removed
trades = [
    ["1", "AAPL", "B", "10", "10"],
    ["2", "AAPL", "S", "10", "15"],
]
expected = [["CASH", "1050"]]
assert buildPortfolio(trades, 0) == expected

# T0-3: multiple symbols, alphabetical output
trades = [
    ["1", "MSFT", "B", "1", "100"],
    ["2", "AAPL", "B", "2", "10"],
]
expected = [["CASH", "880"], ["AAPL", "2"], ["MSFT", "1"]]
assert buildPortfolio(trades, 0) == expected


# ---------- Follow-up 1 (Margin call, no collateral) ----------
# T1-1: given margin call example
trades = [
    ["1", "AAPL", "B", "10", "100"],  # cash=0
    ["2", "AAPL", "S", "2", "80"],    # cash=160, AAPL=8, last(AAPL)=80
    ["3", "GOOG", "B", "15", "20"],   # cash=-140 -> margin call sells AAPL(80) 2 shares
]
expected = [["CASH", "20"], ["AAPL", "6"], ["GOOG", "15"]]
assert buildPortfolio(trades, 1) == expected

# T1-2: tie on price => alphabetical symbol first
trades = [
    ["1", "AAPL", "B", "5", "100"],   # cash=500, AAPL=5
    ["2", "ABPL", "B", "5", "100"],   # cash=0, ABPL=5
    ["3", "GOOG", "B", "1", "50"],    # cash=-50 -> sell AAPL first (tie price=100)
]
expected = [["CASH", "50"], ["AAPL", "4"], ["ABPL", "5"], ["GOOG", "1"]]
assert buildPortfolio(trades, 1) == expected

# T1-3: margin call can sell shares of just-bought stock
trades = [
    ["1", "AAPL", "B", "1", "10"],    # cash=990, AAPL=1
    ["2", "GOOG", "B", "100", "20"],  # cash=-1010 -> sell GOOG 51 shares at 20 => cash=10
]
expected = [["CASH", "10"], ["AAPL", "1"], ["GOOG", "49"]]
assert buildPortfolio(trades, 1) == expected


# ---------- Follow-up 2 (Margin call + collateral + no-alternating) ----------
# Uses your provided examples.

# T2-1: Example 1
trades = [
    ["1", "AAPL",  "B", "5", "100"],
    ["2", "GOOG",  "B", "5", "60"],
    ["3", "GOOGO", "B", "5", "40"],  # special, collateral=GOOG
    ["5", "AAPLO", "B", "5", "30"],  # special, collateral=AAPL
]
expected = [["CASH", "10"], ["AAPL", "5"], ["AAPLO", "5"], ["GOOG", "5"], ["GOOGO", "1"]]
assert buildPortfolio(trades, 2) == expected

# T2-2: Example 2
trades = [
    ["1", "AAPL",  "B", "8",  "100"],
    ["2", "AAPLO", "B", "5",  "40"],
    ["3", "GOOG",  "B", "20", "30"],
]
expected = [["CASH", "0"], ["AAPL", "4"], ["GOOG", "20"]]
assert buildPortfolio(trades, 2) == expected

# T2-3: Example 3
trades = [
    ["1", "AAPL",  "B", "6",  "100"],
    ["2", "GOOG",  "B", "5",  "60"],
    ["3", "GOOGO", "B", "5",  "40"],
    ["5", "AAPLO", "B", "5",  "30"],
]
expected = [["CASH", "10"], ["AAPL", "5"], ["AAPLO", "5"], ["GOOG", "5"], ["GOOGO", "1"]]
assert buildPortfolio(trades, 2) == expected


print("All tests passed!")

