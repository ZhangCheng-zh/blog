"""
source:
https://www.hack2hire.com/companies/robinhood/coding-questions/67e4c55150b60b77022f3867/practice?questionId=67e8af3a7131f7c901ffd7a1

You are given a list of order records for a single stock. Each record is a list containing the limit price (a number), quantity (number of shares), and order type (either "buy" or "sell").

Your task is to calculate the total number of shares traded based on the following rules:

A buy order can be matched with a sell order if the sell price is less than or equal to the buy price.
A sell order can be matched with a buy order if the buy price is greater than or equal to the sell price.
If no matching order exists, the order is stored until a matching counter-order arrives.
Orders must be matched at the best possible price:
Buy orders match with the lowest sell price available.
Sell orders match with the highest buy price available.
Orders may be partially filled if the available quantity is less than the order's quantity.
Return the total number of shares successfully traded.

Example 1:
Input: orders = [["150", "5", "buy"],["190", "1", "sell"],["200", "1", "sell"],["100", "9", "buy"],["140", "8", "sell"],["210", "4", "buy"]]
Output: 9
Explanation: There's no trade in the first four orders. Trading begins with the fifth order, a sell at 140 for 8 shares, which matches a stored buy order at 150, executing 5 shares. The sixth order, a buy at 210 for 4 shares, then triggers trading by matching the remaining 3 shares from the sell at 140 and 1 share from the sell at 190. In total, 5 + 4 = 9 shares are traded.

Example 2:
Input: orders = [["100","10","buy"],["105","5","buy"],["110","8","buy"]]
Output: 0

Example 3:
Input: orders = [["120","10","buy"],["115","5","sell"],["110","3","sell"]]
Output: 8

"""
import heapq
def findMaxTradeShares(orders):
    # maintain two books:
    # maxheap for buy order
    # minheap for sell order

    # matching rules
    # incoming buy matches lowest sell while sellPrice <= buyPrice
    # incoming sell matches highest buy while buyPrice >= sellPrice

    bq = [] # buy heap
    sq = [] # sell heap
    res = 0
    
    # time O(nlgn) n is length of order
    # space O(n)
    for price, cnt, type in orders:
        price = int(price)
        cnt = int(cnt)

        if type == 'buy':
            while cnt > 0 and sq and sq[0][0] <= price: # have sell order match
                sellPrice, sellCnt = heapq.heappop(sq)
                m = min(cnt, sellCnt)
                res += m
                cnt -= m
                sellCnt -= m
                if sellCnt > 0:
                    heapq.heappush(sq, (sellPrice, sellCnt))
            
            if cnt > 0:
                heapq.heappush(bq, (-price, cnt))
        
        else: # sell
            while cnt > 0 and bq and -bq[0][0] >= price:
                buyPriceNeg, buyCnt = heapq.heappop(bq)
                m = min(cnt, buyCnt)
                res += m
                cnt -= m
                buyCnt -= m
                if buyCnt > 0:
                    heapq.heappush(bq, (buyPriceNeg, buyCnt))
            
            if cnt > 0:
                heapq.heappush(sq, (price, cnt))
        
    return res


assert findMaxTradeShares([["150","5","buy"],["190","1","sell"],["200","1","sell"],["100","9","buy"],["140","8","sell"],["210","4","buy"]]) == 9
assert findMaxTradeShares([["100","10","buy"],["105","5","buy"],["110","8","buy"]]) == 0
assert findMaxTradeShares([["120","10","buy"],["115","5","sell"],["110","3","sell"]]) == 8

