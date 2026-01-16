"""
Best Currency Exchange Rate
You are given exchange rates between currencies.
fromArr[i] -> toArr[i] has rate rateArr[i]

Rates work both ways:
if A -> B = r, then B -> A = 1 / r
You can convert through multiple currencies.
A path A -> X -> Y -> B has rate = (A->X) * (X->Y) * (Y->B)

Task
For each query (from, to), return the maximum exchange rate you can get by choosing the best path.
If from or to doesn’t exist, or no path connects them, return -1.0.

Implement
CurrencyConverter(fromArr, toArr, rateArr)
build the converter
getBestRate(from, to) -> double

return best rate from from to to

Example
Rates:
GBP -> JPY = 155
USD -> JPY = 112
USD -> GBP = 0.9

Query: USD -> JPY
Direct: 112
Indirect: USD -> GBP -> JPY = (1/0.9) * 155 = 139.5
Answer: 139.5
"""
from collections import defaultdict
class CurrencyConverter:
    def __init__(self, fromArr, toArr, rateArr):
        self.g = defaultdict(list)

        for a, b,r in zip(fromArr, toArr, rateArr):
            self.g[a].append((b, r))
            self.g[b].append((a, 1.0 / r))
    
    def getBestRate(self, fromCurrency, toCurrency):
        if fromCurrency not in self.g or toCurrency not in self.g:
            return -1.0
        
        if fromCurrency == toCurrency:
            return 1.0
        
        visited = set()

        def dfs(cur, rateSoFar):
            if cur == toCurrency:
                return rateSoFar

            visited.add(cur)
            best = -1.0

            for nxt, r in self.g[cur]:
                if nxt in visited:
                    continue
                best = max(best, dfs(nxt, rateSoFar*r))
            
            visited.remove(cur)
            return best

        return dfs(fromCurrency, 1.0)
    
def runTests():
    # Example from prompt
    fromArr = ["GBP", "USD", "USD", "USD", "CNY"]
    toArr   = ["JPY", "JPY", "GBP", "CAD", "EUR"]
    rateArr = [155.0, 112.0, 0.9, 1.3, 0.14]

    cc = CurrencyConverter(fromArr, toArr, rateArr)

    # 1) Better indirect path
    assert abs(cc.getBestRate("USD", "JPY") - 139.5) < 1e-9

    # 2) Reverse direction via inverse edges:
    # JPY -> USD = 1/112, USD -> GBP = 0.9  => 0.9/112
    assert abs(cc.getBestRate("JPY", "GBP") - (0.9 / 112.0)) < 1e-12

    # 3) Currency not present
    assert cc.getBestRate("XYZ", "GBP") == -1.0

    # 4) No path exists (CNY only connects to EUR)
    assert cc.getBestRate("CNY", "CAD") == -1.0

    # 5) Same currency
    assert cc.getBestRate("USD", "USD") == 1.0

    # Extra: direct beats indirect
    fromArr2 = ["A", "B", "A"]
    toArr2   = ["B", "C", "C"]
    rateArr2 = [2.0, 2.0, 10.0]  # A->C direct is 10, indirect A->B->C is 4
    cc2 = CurrencyConverter(fromArr2, toArr2, rateArr2)
    assert abs(cc2.getBestRate("A", "C") - 10.0) < 1e-9

    # Extra: indirect beats direct
    fromArr3 = ["A", "A", "B"]
    toArr3   = ["C", "B", "C"]
    rateArr3 = [3.0, 2.0, 2.0]   # A->C direct is 3, indirect A->B->C is 4
    cc3 = CurrencyConverter(fromArr3, toArr3, rateArr3)
    assert abs(cc3.getBestRate("A", "C") - 4.0) < 1e-9

    print("All tests passed!")


runTests()
