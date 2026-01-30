"""
Question: Minimum Cost to Buy All Words with Prefix Bundles
You are given a list of distinct words. You want to “buy” all of them with minimum total cost.
You have two types of purchases:
Buy a single word
You can buy a specific word w for cost wordCost[w].
Buy a prefix bundle
You can buy a bundle for a prefix p for cost bundleCost[p].
Buying prefix p purchases all words that start with p.
You may buy any combination of single words and prefix bundles.
A word is considered purchased if it is covered by at least one purchase (either directly or by a prefix bundle).

Goal
Return the minimum total cost to purchase all words.

Input
words: List[str] — list of words to purchase
wordCost: Dict[str, int] — cost to buy each word individually
bundleCost: Dict[str, int] — cost to buy each prefix bundle (prefix can be any length)

Output
minTotalCost: int

Notes / Assumptions
All costs are non-negative integers.
Every word in words exists as a key in wordCost.
bundleCost may contain prefixes that match no word; those bundles are useless and can be ignored.

Output only the minimum total cost (no need to output which purchases were made).
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.wordCost = None
        self.bundleCost = None
    
def minCostBuyAllWords(words, wordCost, bundleCost):
    root = TrieNode()

    # Insert all words
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        # reach the end letter of word, add wordCost
        node.wordCost = wordCost[w]

    # Insert all bundle prefixes (even if no word currently matches)
    for prefix, cost in bundleCost.items():
        node = root
        for ch in prefix:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.bundleCost = cost if node.bundleCost is None else min(node.bundleCost, cost)

    def dfs(node):
        # if node is complete word node, update baseCost
        baseCost = (node.wordCost or 0)
        # sum all children's cost
        for child in node.children.values():
            baseCost += dfs(child)

        if node.bundleCost is None:
            return baseCost
        # compare prefix cost and all individual child cost
        return min(baseCost, node.bundleCost)

    return dfs(root)
    
# ---------- Test cases ----------
def runTests() -> None:
    # 1) No bundles -> must buy all singles
    words = ["photo", "phoeo", "phose", "phcertd"]
    wordCost = {"photo": 5, "phoeo": 6, "phose": 4, "phcertd": 20}
    bundleCost = {}
    assert minCostBuyAllWords(words, wordCost, bundleCost) == 35

    # 2) Simple prefix bundles (like your 3-letter example)
    bundleCost2 = {"pho": 12, "phc": 15}
    # pho group singles = 15, choose 12; phc single 20, choose 15 => 27
    assert minCostBuyAllWords(words, wordCost, bundleCost2) == 27

    # 3) Nested prefixes: 4-letter bundles inside 3-letter group
    bundleCost3 = {
        "pho": 12,
        "phot": 3,   # covers photo only
        "phoe": 10,  # covers phoeo only
        "phos": 100, # covers phose only (too expensive)
        "phc": 15,
        "phce": 8,   # covers phcertd cheaper
    }
    # pho: min(12, 3 + 6 + 4 = 13) => 12
    # phc: min(15, 8) => 8
    # total = 20
    assert minCostBuyAllWords(words, wordCost, bundleCost3) == 20

    # 4) Word is prefix of another word
    words4 = ["a", "ab", "abc"]
    wordCost4 = {"a": 5, "ab": 6, "abc": 7}
    bundleCost4 = {"a": 10, "ab": 3}
    # best: buy "ab" bundle = 3 (covers ab, abc) + buy "a" single = 5 => 8
    assert minCostBuyAllWords(words4, wordCost4, bundleCost4) == 8

    # 5) Bundle equals single sum -> either is fine, min same
    words5 = ["aa", "ab"]
    wordCost5 = {"aa": 4, "ab": 6}
    bundleCost5 = {"a": 10}
    assert minCostBuyAllWords(words5, wordCost5, bundleCost5) == 10

    # 6) Useless bundle (prefix matches no word path) should be ignored
    words6 = ["cat", "car"]
    wordCost6 = {"cat": 7, "car": 5}
    bundleCost6 = {"dog": 1, "ca": 20}
    # "dog" ignored, "ca" too expensive => buy singles: 12
    assert minCostBuyAllWords(words6, wordCost6, bundleCost6) == 12

    # 7) Deep bundle wins (covers multiple words under it)
    words7 = ["abcd", "abce", "abcf", "ax"]
    wordCost7 = {"abcd": 5, "abce": 5, "abcf": 5, "ax": 100}
    bundleCost7 = {"abc": 9, "a": 50}
    # For "abc" subtree: 9 vs 15 => 9, plus "ax" is 100, compare with bundle "a"=50
    # If buy "a" bundle => 50 (covers everything) which is best
    assert minCostBuyAllWords(words7, wordCost7, bundleCost7) == 50

    # 8) Single-character bundle
    words8 = ["x", "xy", "xyz"]
    wordCost8 = {"x": 10, "xy": 10, "xyz": 10}
    bundleCost8 = {"x": 15, "xy": 12}
    # xy covers xy+xyz for 12, plus x single 10 => 22 vs x bundle 15 => choose 15
    assert minCostBuyAllWords(words8, wordCost8, bundleCost8) == 15

    print("All tests passed!")


if __name__ == "__main__":
    runTests()