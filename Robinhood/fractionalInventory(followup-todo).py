"""
## Fractional Shares Inventory (Robinhood)

You are given:
* `orders`: list of orders, each is
  `["SYMBOL", "B" or "S", "QUANTITY", "UNIT_PRICE"]`
* `inventory`: initial fractional inventory, each is
  `["SYMBOL", "FRACTION"]`

All numbers are **integers scaled by 100** (last 2 digits are decimals):
* `"42"` = 0.42
* `"100"` = 1.00
* `UNIT_PRICE` is price per 1 share (scaled by 100)

`QUANTITY` can be:
* a share amount like `"42"` (0.42 shares), or
* a dollar amount like `"$42"` ($0.42), which must be converted to shares using `UNIT_PRICE`.

### Rules (process orders in given order)
For each order on symbol `X`:
* **Buy ("B")**: customer buys shares
  * Use inventory first.
  * If inventory is not enough, Robinhood buys whole shares from the market to cover the shortage and keeps any leftover fractional part in inventory.
* **Sell ("S")**: customer sells shares
  * Add the sold shares into inventory.

After each order, **flatten** inventory for that symbol:
* inventory must be **non-negative**
* inventory must be **< 1.00 share**
(if inventory becomes `>= 1.00`, sell whole shares to the market to reduce it)

### Output
Return the final `inventory` list in the **same order and format** as the input inventory:
`["SYMBOL", "FRACTION"]` (still scaled by 100).

fractional sharing，就是input有些变化，每个order和inventory的元素都变成string，然后内部通过 / 分隔。
"""

# result is real fraction share * 100
def parseQtyToShare100(qty, price100Str):
    if qty.startswith('$'): # qty is money
        dollars100 = int(qty[1:])
        price100 = int(price100Str)
        if price100 == 0:
            return 0
        return (dollars100 * 100) // price100
    return int(qty)

def processOrders(orders, inventory):
    invMap = {}
    invOrder = [sym for sym, _ in inventory]

    for sym, qty in inventory:
        invMap[sym] = int(qty) % 100
    
    for sym, orderType, qty, price100 in orders:
        if sym not in invMap:
            invMap[sym] = 0
        
        qty100 = parseQtyToShare100(qty, price100)

        if orderType == 'B':
            invMap[sym] = (invMap[sym] - qty100) % 100
        else:
            invMap[sym] = (invMap[sym] + qty100) % 100
    
    return [[sym, str(invMap[sym])] for sym in invOrder]


# All-in-one test cases (orders, inventory, expected)
testCases = [
    {
        "name": "T1_buy_from_inventory_only",
        "orders": [["AAPL","B","42","100"]],
        "inventory": [["AAPL","99"]],
        "expected": [["AAPL","57"]],
    },
    {
        "name": "T2_dollar_buy_from_inventory",
        "orders": [["AAPL","B","$42","100"]],
        "inventory": [["AAPL","50"]],
        "expected": [["AAPL","8"]],
    },
    {
        "name": "T3_buy_needs_market_whole_share",
        "orders": [["AAPL","B","50","100"]],
        "inventory": [["AAPL","20"]],
        "expected": [["AAPL","70"]],
    },
    {
        "name": "T4_sell_causes_flatten",
        "orders": [["AAPL","S","75","100"], ["AAPL","S","50","100"]],
        "inventory": [["AAPL","0"]],
        "expected": [["AAPL","25"]],
    },
    {
        "name": "T5_buy_sell_buy_multiple_steps",
        "orders": [["AAPL","B","80","100"], ["AAPL","S","50","100"], ["AAPL","B","10","100"]],
        "inventory": [["AAPL","60"]],
        "expected": [["AAPL","20"]],
    },
    {
        "name": "T6_dollar_buy_non_1_price_exact_division",
        "orders": [["AAPL","B","$100","200"]],  # $1.00 @ $2.00 => 0.50 shares
        "inventory": [["AAPL","10"]],
        "expected": [["AAPL","60"]],
    },
    {
        "name": "T7_multiple_symbols_keep_inventory_order",
        "orders": [["AAPL","B","50","100"], ["GOOG","S","80","100"]],
        "inventory": [["AAPL","30"], ["GOOG","90"]],
        "expected": [["AAPL","80"], ["GOOG","70"]],
    },
    {
        "name": "T8_zero_quantity_noop",
        "orders": [["AAPL","B","0","100"], ["AAPL","S","0","100"]],
        "inventory": [["AAPL","55"]],
        "expected": [["AAPL","55"]],
    },
]



def runTests():
    for t in testCases:
        got = processOrders(t["orders"], t["inventory"])
        assert got == t["expected"], f'{t["name"]} FAILED\n got={got}\n exp={t["expected"]}'
    print("All tests passed!")

runTests()