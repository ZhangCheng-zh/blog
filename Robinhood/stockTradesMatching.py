"""
## Stock Trades Matching (Robinhood)

A trade is a fixed-width string with 4 comma-separated fields:

`"<SYMBOL>,<SIDE>,<QTY>,<ID>"`

* `SYMBOL`: 4 characters, uppercase letters, **left-padded with spaces** (e.g. `"  FB"`, `"AAPL"`)
* `SIDE`: `"B"` (buy) or `"S"` (sell)
* `QTY`: 4 digits, **left-padded with zeros** (e.g. `"0010"`)
* `ID`: 6 alphanumeric characters

Example:
`"AAPL,B,0100,ABC123"`
---
### Input
* `house_trades: List[str]`
* `street_trades: List[str]`
Trades are **distinct but not unique** (duplicates may exist).
---

### Matching Rules (apply in this priority order)

1. **Exact Match (highest priority)**
   Match one house trade with one street trade if **all 4 fields are identical**:
   `SYMBOL, SIDE, QTY, ID`

2. **Fuzzy Match (follow-up 1)**
   After all exact matches are removed, match one house trade with one street trade if:

* `SYMBOL, SIDE, QTY` are identical
* `ID` is ignored

Tie-break (when multiple possible matches):

* match the **alphabetically earliest** remaining house trade with the **alphabetically earliest** remaining street trade

3. **Offsetting Match (follow-up 2)**
   After exact + fuzzy matches are removed, match trades **within the same list** (house with house, or street with street) if:

* `SYMBOL` and `QTY` are identical
* `SIDE` is opposite (`B` vs `S`)

Tie-break:

* match the **alphabetically earliest buy** with the **alphabetically earliest sell**

---

### Output

Return all **unmatched** trades from both lists as:

* `List[str]` sorted in **ascending lexicographical order** (string order)

---

### Examples

#### TEST1 (Exact match)

```text
house_trades  = ["AAPL,B,0100,ABC123", "GOOG,S,0050,CDC333"]
street_trades = ["  FB,B,0100,GBGGGG", "AAPL,B,0100,ABC123"]

output = ["  FB,B,0100,GBGGGG", "GOOG,S,0050,CDC333"]
```

#### TEST2 (Duplicates + exact match)

```text
house_trades  = ["AAPL,S,0010,ZYX444",
                 "AAPL,S,0010,ZYX444",
                 "AAPL,B,0010,ABC123",
                 "GOOG,S,0050,GHG545"]
street_trades = ["GOOG,S,0050,GHG545",
                 "AAPL,S,0010,ZYX444",
                 "AAPL,B,0010,TTT222"]

output = ["AAPL,S,0010,ZYX444"]
```

#### TEST3 (Multiple duplicates)

```text
house_trades  = ["AAPL,B,0100,ABC123",
                 "AAPL,B,0100,ABC123",
                 "AAPL,B,0100,ABC123",
                 "GOOG,S,0050,CDC333"]
street_trades = ["  FB,B,0100,GBGGGG",
                 "AAPL,B,0100,ABC123"]

output = ["  FB,B,0100,GBGGGG",
          "AAPL,B,0100,ABC123",
          "AAPL,B,0100,ABC123",
          "GOOG,S,0050,CDC333"]
```
"""
from collections import Counter, defaultdict
from typing import List, Tuple, Dict

def getUnmatchedTrades(houseTrades, streetTrades):
    house = Counter(houseTrades)
    street = Counter(streetTrades)

    cache = {}

    def parse(t):
        if t not in cache:
            cache[t] = tuple(t.split(','))
        return cache[t]
    
    def dec(cnt, key, k):
        if k <= 0:
            return
        newv = cnt[key] - k 
        if newv <= 0:
            cnt.pop(key, None) # del cnt[key]
        else:
            cnt[key] = newv

    # exact match    
    for t in list(house.keys() & street.keys()):
        m = min(house[t], street[t])
        dec(house, t, m)
        dec(street, t, m)
    

    # fuzzy matches
    def groupByFuzzy(cnt):
        groups = defaultdict(list)
        for t, c in cnt.items():
            sym, side, qty, _ = parse(t)
            groups[(sym, side, qty)].append([t, c])
        for k in groups:
            # sort list in same key with lexico order of order strs
            groups[k].sort(key = lambda x: x[0])
        return groups
    
    houseF = groupByFuzzy(house)
    streetF = groupByFuzzy(street)

    for k in (houseF.keys() & streetF.keys()):
        hlist = houseF[k]
        slist = streetF[k]
        i = j = 0
        while i < len(hlist) and j < len(slist):
            ht, hc = hlist[i]
            st, sc = slist[j]
            m = min(hc, sc)

            dec(house, ht, m)
            dec(street, st, m)

            hc -= m
            sc -= m 
            hlist[i][1] = hc
            slist[j][1] = sc 

            if hc == 0:
                i += 1
            if sc == 0:
                j += 1
    
    # offsetting matches
    def offsetWithOneSide(cnt):
        buys = defaultdict(list) # (sym, qty) -> [[tradeStr, count], ... ]
        sells = defaultdict(list)

        for t, c in cnt.items():
            sym, side, qty, _ = parse(t)
            key = (sym, qty)

            (buys if side == 'B' else sells)[key].append([t, c])

        
        for k in buys:
            buys[k].sort(key = lambda x: x[0])
        
        for k in sells:
            sells[k].sort(key = lambda x: x[0])
        
        for key in (buys.keys() & sells.keys()):
            blist = buys[key]
            slist = sells[key]
            i = j = 0
            while i < len(blist) and j < len(slist):
                bt, bc = blist[i]
                st, sc = slist[j]
                m = min(bc, sc)

                dec(cnt, bt, m)
                dec(cnt, st, m)
                bc -= m
                sc -= m 
                blist[i][1] = bc 
                slist[j][1] = sc

                if bc == 0:
                    i += 1
                if sc == 0:
                    j += 1

    offsetWithOneSide(house)
    offsetWithOneSide(street)


    res = []
    for t, c in house.items():
        res.extend([t] * c)
    
    for t, c in street.items():
        res.extend([t] * c)
    
    res.sort()
    return res



testCases = [
    # Tests 1-5: Exact
    {
        "name": "TEST1_exact_basic",
        "house_trades": ["AAPL,B,0100,ABC123", "GOOG,S,0050,CDC333"],
        "street_trades": ["  FB,B,0100,GBGGGG", "AAPL,B,0100,ABC123"],
        "expected": ["  FB,B,0100,GBGGGG", "GOOG,S,0050,CDC333"],
    },
    {
        "name": "TEST2_exact_duplicates",
        "house_trades": [
            "AAPL,S,0010,ZYX444",
            "AAPL,S,0010,ZYX444",
            "AAPL,B,0010,ABC123",
            "GOOG,S,0050,GHG545",
        ],
        "street_trades": [
            "GOOG,S,0050,GHG545",
            "AAPL,S,0010,ZYX444",
            "AAPL,B,0010,TTT222",
        ],
        "expected": ["AAPL,S,0010,ZYX444"],
    },
    {
        "name": "TEST3_exact_more_duplicates",
        "house_trades": [
            "AAPL,B,0100,ABC123",
            "AAPL,B,0100,ABC123",
            "AAPL,B,0100,ABC123",
            "GOOG,S,0050,CDC333",
        ],
        "street_trades": ["  FB,B,0100,GBGGGG", "AAPL,B,0100,ABC123"],
        "expected": [
            "  FB,B,0100,GBGGGG",
            "AAPL,B,0100,ABC123",
            "AAPL,B,0100,ABC123",
            "GOOG,S,0050,CDC333",
        ],
    },
    {
        "name": "TEST4_exact_no_match_all_returned_sorted",
        "house_trades": ["AAPL,B,0100,AAA111", "GOOG,S,0050,BBB222"],
        "street_trades": ["MSFT,B,0001,CCC333"],
        "expected": ["AAPL,B,0100,AAA111", "GOOG,S,0050,BBB222", "MSFT,B,0001,CCC333"],
    },
    {
        "name": "TEST5_exact_multiple_exact_pairs_leftover",
        "house_trades": ["AAPL,B,0100,AAA111", "AAPL,B,0100,AAA111", "AAPL,S,0100,AAA111"],
        "street_trades": ["AAPL,B,0100,AAA111", "AAPL,S,0100,AAA111"],
        "expected": ["AAPL,B,0100,AAA111"],
    },

    # Tests 6-9: Fuzzy
    {
        "name": "TEST6_fuzzy_simple_id_diff",
        "house_trades": ["AAPL,B,0100,AAA111"],
        "street_trades": ["AAPL,B,0100,BBB222"],
        "expected": [],
    },
    {
        "name": "TEST7_fuzzy_exact_has_priority",
        "house_trades": ["AAPL,B,0100,AAA111", "AAPL,B,0100,BBB222"],
        "street_trades": ["AAPL,B,0100,AAA111"],
        "expected": ["AAPL,B,0100,BBB222"],
    },
    {
        "name": "TEST8_fuzzy_tie_break_earliest_alpha",
        "house_trades": ["AAPL,B,0100,BBB222", "AAPL,B,0100,AAA111"],
        "street_trades": ["AAPL,B,0100,DDD444", "AAPL,B,0100,CCC333"],
        "expected": [],
    },
    {
        "name": "TEST9_fuzzy_with_counts_earliest_consumed_first",
        "house_trades": ["AAPL,B,0100,AAA111", "AAPL,B,0100,AAA111", "AAPL,B,0100,BBB222"],
        "street_trades": ["AAPL,B,0100,BBB999", "AAPL,B,0100,BBB999"],
        "expected": ["AAPL,B,0100,BBB222"],
    },

    # Test 10: Offsetting
    {
        "name": "TEST10_offsetting_within_house",
        "house_trades": ["AAPL,B,0100,AAA111", "AAPL,S,0100,ZZZ999", "AAPL,S,0100,BBB222"],
        "street_trades": [],
        "expected": ["AAPL,S,0100,ZZZ999"],
    },
]


def runTests():
    for t in testCases:
        got = getUnmatchedTrades(t["house_trades"], t["street_trades"])
        assert got == t["expected"], f'{t["name"]} FAILED\n got={got}\n exp={t["expected"]}'
    print("All tests passed!")


runTests()