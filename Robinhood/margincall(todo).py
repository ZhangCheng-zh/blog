"""
  /*
        Our goal is to build a simplified version of a real Robinhood system that reads a customer's trades from a stream, maintains what they own, and rectifies running out of cash (through a process called a "margin call", which we'll define later). We’re looking for clean code, good naming, testing, etc. We're not particularly looking for the most performant solution.

    **Step 1 (tests 1-4): Parse trades and build a customer portfolio**

    Your input will be a list of trades, each of which is itself a list of strings in the form [timestamp, symbol, B/S (for buy/sell), quantity, price], e.g.

    [["1", "AAPL", "B", "10", "10"], ["3", "GOOG", "B", "20", "5"], ["10", "AAPL", "S", "5", "15"]]

    is equivalent to buying 10 shares (i.e. units) of AAPL for 5 each at timestamp 3, and selling 5 shares of AAPL for $15 at timestamp 10.

    **Input assumptions:**

    - The input is sorted by timestamp
    - All numerical values are nonnegative integers
    - Trades will always be valid (i.e. a customer will never sell more of a stock than they own).

    From the provided list of trades, our goal is to maintain the customer's resulting portfolio (meaning everything they own), **assuming they begin with $1000**. For instance, in the above example, the customer would end up with $875, 5 shares of AAPL, and 20 shares of GOOG. You should return a list representing this portfolio, formatting each individual position as a list of strings in the form [symbol, quantity], using 'CASH' as the symbol for cash and sorting the remaining stocks alphabetically based on symbol. For instance, the above portfolio would be represented as

    [["CASH", "875"], ["AAPL", "5"], ["GOOG", "20"]]

    **Step 2 (tests 5-7): Margin calls**

    If the customer ever ends up with a negative amount of cash **after a buy**, they then enter a process known as a **margin call** to correct the situation. In this process, we forcefully sell stocks in the customer's portfolio (sometimes including the shares we just bought) until their cash becomes non-negative again.

    We sell shares from the most expensive to least expensive shares (based on each symbol's most-recently-traded price) with ties broken by preferring the alphabetically earliest symbol. Assume we're able to sell any number of shares in a symbol at that symbol's most-recently-traded price.

    For example, for this input:

    ```
    [["1", "AAPL", "B", "10", "100"],
    ["2", "AAPL", "S", "2", "80"],
    ["3", "GOOG", "B", "15", "20"]]

    ```

    The customer would be left with 8 AAPL shares, 15 GOOG shares, and 80 a share) to cover the deficit. Afterwards, they would have 6 shares of AAPL, 15 shares of GOOG, and a cash balance of $20.

    The expected output would be

    [["CASH", "20"], ["AAPL", "6"], ["GOOG", "15"]]

    **Step 3/Extension 1 (tests 8-10): Collateral**

    Certain stocks have special classifications, and require the customer to also own another "collateral" stock, meaning it cannot be sold during the margin call process. Our goal is to handle a simplified version of this phenomenon.

    Formally, we'll consider stocks with symbols ending in "O" to be special, with the remainder of the symbol identifying its collateral stock. For example, AAPLO is special, and its collateral stock is AAPL. **At all times**, the customer must hold at least as many shares of the collateral stock as they do the special stock; e.g. they must own at least as many shares of AAPL as they do of AAPLO.

    As a result, the margin call process will now sell the most valuable **non-collateral** share until the balance is positive again. Note that if this sells a special stock, some of the collateral stock may be freed up to be sold.

    For example, if the customer purchases 5 shares of AAPL for 75 each, then finally 5 shares of AAPLO for 125, but their shares of AAPL can no longer be used to cover the deficit (since they've become collateral for AAPLO). As a result, 2 shares of GOOG would be sold back (again at 25, 5 AAPL, 5 AAPLO, and 3 GOOG. Thus, with an input of

    [["1", "AAPL", "B", "5", "100"], ["2", "GOOG", "B", "5", "75"], ["3", "AAPLO", "B", "5", "50"]]

    the corresponding output would be

    [["CASH", "25"], ["AAPL", "5"], ["AAPLO", "5"], ["GOOG", "3"]
    */


// class User {
//   private:
//     // Skip user info fields
//     // ...
//     vector<vector<string>> records;
    
//   public:
//     User(vector<vector<string>>& records) : this->records(records);
// };

const string kCash = "CASH";
const int kCashAmount = 1000;

void tradeStock(map<string, int>& symbol2shares,
                const string& symbol,
                const int price,
                const int quantity,
                const string ops,
                int& cash) {
  if (ops == "B") { // Buy order
      cash -= price * quantity;
      symbol2shares[symbol] += quantity;
  } else if (ops == "S") {
      cash += price * quantity;
      symbol2shares[symbol] -= quantity;           
  } else {
      // Invalid operation type
      assert(false);
  }
}

void getUserPortfolio(vector<vector<string>>& records,
                      vector<vector<string>>& portfolio) {
  portfolio.clear();
  map<string/*symbol*/, int/*shares*/> symbol2shares;
  // Init map with initial cash
  int cash = kCashAmount;
  // Parse each record
  for (auto& record : records) {
      assert(record.size() == 5);
      string& symbol = record[1], &ops = record[2];
      int quantity = stoi(record[3]), price = stoi(record[4]);
      tradeStock(symbol2shares, symbol, price, quantity, ops, cash);
  }
  portfolio.push_back( {kCash, to_string(cash)} );
  for (auto it = symbol2shares.begin(); it != symbol2shares.end(); it++) {
    // Do not output stocks with zero shares
    if (it->second) {
      portfolio.push_back({ it->first, to_string(it->second) });
    }
  }
}





// ***************************** //
void marginCall(map<string, int>& symbol2shares,
                map<string, int>& symbol2price,
                int& cash) {
  if (cash >= 0) {
    return;
  }
  
  typedef pair<int/*price*/, string/*symbol*/> Stock;
  // Sort stocks by prices(high to low), and then sort in alphabetical order if tie
  // Define custom comparator
  auto comp = [](const Stock& A, const Stock& B) {
    return A.first == B.first ? A.second < B.second : A.first > B.first;
  };
  set<Stock, decltype(comp)> sorted_stocks(comp);
  for (auto it = symbol2price.begin(); it != symbol2price.end(); it++) {
    sorted_stocks.emplace(it->second, it->first);
  }
  // Keep selling until cash becomes non-negative
  while (cash < 0) {
    auto it = sorted_stocks.begin();
    const string symbol = it->second;
    // Sell all or sell enough to cover the deflict
    int sell_quantity = min(symbol2shares[symbol], (int)ceil((-cash) * 1.0 / it->first));
    tradeStock(symbol2shares, symbol, it->first, sell_quantity, "S", cash);
    if (symbol2shares[symbol] == 0) {
      symbol2shares.erase(symbol);
      symbol2price.erase(symbol);
      sorted_stocks.erase(it);
    }
  }
}

void getUserPortfolioWithMarginCall(vector<vector<string>>& records,
                                    vector<vector<string>>& portfolio) {
  portfolio.clear();
  map<string/*symbol*/, int/*shares*/> symbol2shares;
  int cash = kCashAmount;
  map<string/*symbol*/, int/*price*/> symbol2price;
  // Parse each record
  for (auto& record : records) {
      assert(record.size() == 5);
      string& symbol = record[1], &ops = record[2];
      int quantity = stoi(record[3]), price = stoi(record[4]);
      // Trade stock
      tradeStock(symbol2shares, symbol, price, quantity, ops, cash);
      // Update price
      symbol2price[symbol] = price;
      // Margin call
      marginCall(symbol2shares, symbol2price, cash);
  }
  portfolio.push_back( {kCash, to_string(cash)} );
  for (auto it = symbol2shares.begin(); it != symbol2shares.end(); it++) {
    // Do not output stocks with zero shares
    if (it->second) {
      portfolio.push_back({ it->first, to_string(it->second) });
    }
  }                   
}



// ***************************** //

bool isGoodtoSell(map<string, int>& symbol2shares,
                  string symbol) {
    // All special stocks are good to sell at any time
    if (symbol.at(symbol.size() - 1) == 'O') {
        return true;
    }
    // Stocks without associated special stock are good to sell at any time
    if (symbol2shares.find(symbol + "O") == symbol2shares.end()) {
        return true;
    }
    // Some collateral stocks have been freed up to sell
    if (symbol2shares[symbol + "O"] < symbol2shares[symbol]) {
        return true;
    }
    return false;
}

void marginCallWithCollateral(map<string, int>& symbol2shares,
                              map<string, int>& symbol2price,
                              int& cash) {
    if (cash >= 0) {
        return;
    }
    // Sort stocks by price
    typedef pair<int/*price*/, string/*symbol*/> Stock;
    auto comp = [](const Stock& A, const Stock& B) {
      return A.first == B.first ? A.second < B.second : A.first > B.first;
    };
    set<Stock, decltype(comp)> sorted_stocks(comp);
    for (auto it = symbol2price.begin(); it != symbol2price.end(); it++) {
        sorted_stocks.emplace(it->second, it->first);
    }
    
    while (cash < 0) {
        auto it = sorted_stocks.begin();
        // To find the one to sell
        while (it != sorted_stocks.end() && !isGoodtoSell(symbol2shares, it->second)) {
            it++;
        }
        assert(it != sorted_stocks.end());
        string symbol = it->second;
        // Sell one share every time
        tradeStock(symbol2shares, symbol, it->first, 1, "S", cash);
        if (symbol2shares[symbol] == 0) {
            symbol2shares.erase(symbol);
            symbol2price.erase(symbol);
            sorted_stocks.erase(it);
        }
    }
}



void getUserPortfolioWithCollateral(const vector<vector<string>>& records,
                                    vector<vector<string>>& portfolio) {
    portfolio.clear();
    map<string, int> symbol2shares;
    map<string, int> symbol2price;
    int cash = kCashAmount;
    
    for (const auto record : records) {
        const string symbol = record[1];
        const int price = stoi(record[4]);
        const int quantity = stoi(record[3]);
        tradeStock(symbol2shares, symbol, price, quantity, record[2], cash);
        // Update stock price
        symbol2price[symbol] = price;
        // Margin call with collateral
        marginCallWithCollateral(symbol2shares, symbol2price, cash);
    }
    portfolio.push_back( {kCash, to_string(cash)} );
    for (auto it = symbol2shares.begin(); it != symbol2shares.end(); it++) {
      // Do not output stocks with zero shares
      if (it->second) {
        portfolio.push_back({ it->first, to_string(it->second) });
      }
    }
}



void print(vector<vector<string>>& portfolio) {
    // auto comp = [](vector<string> A, vector<string> B) {
    //     return A[0] < B[0];
    // };
    // sort(portfolio.begin(), portfolio.end(), comp);
    for (const auto& p : portfolio) {
        cout << "\n[" << p[0] << ", " << p[1] << "]";
    }
    cout << endl;
}

int main() {
    vector<vector<string>> records = {
        {"1", "AAPL", "B", "10", "10"},
        {"3", "GOOG", "B", "20", "5"},
        {"10", "AAPL", "S", "5", "15"}
    };
    vector<vector<string>> portfolio;
    getUserPortfolio(records, portfolio);
    cout << "Q1 test case 0: ";
    print(portfolio);
    
    records = {
        {"1", "AAPL", "B", "10", "10"},
        {"3", "GOOG", "B", "20", "5"},
        {"4", "  FB", "B", "5", "12"},
        {"3", "GOOG", "S", "3", "8"},
        {"3", "GOOG", "B", "5", "10"},
        {"10", "AAPL", "S", "5", "15"}
    };
    getUserPortfolio(records, portfolio);
    cout << "\nQ1 test case 1: ";
    print(portfolio);
    
    records = {
        {"1", "AAPL", "B", "10", "100"},
        {"2", "AAPL", "S", "2", "80"},
        {"3", "GOOG", "B", "15", "20"}
    };
    getUserPortfolioWithMarginCall(records, portfolio);
    cout << "\nQ2 test case 1: ";
    print(portfolio);
    
    records = {
        {"1", "AAPL", "B", "5", "100"},
        {"2", "ABPL", "B", "5", "100"},
        {"3", "AAPL", "S", "2", "80"},
        {"4", "ABPL", "S", "2", "80"},
        // has tie on price, take alpha first
        {"5", "GOOG", "B", "15", "30"}
    };
    getUserPortfolioWithMarginCall(records, portfolio);
    cout << "\nQ2 test case 2: ";
    print(portfolio);
    
    records = {
        {"1", "AAPL", "B", "5", "100"},
        {"2", "ABPL", "B", "5", "100"},
        {"3", "AAPL", "S", "2", "80"},
        {"4", "ABPL", "S", "2", "120"},
        // pick high price first
        {"5", "GOOG", "B", "15", "30"}
    };
    getUserPortfolioWithMarginCall(records, portfolio);
    cout << "\nQ2 test case 3: ";
    print(portfolio);
    
    records = {
            {"1", "AAPL", "B", "5", "100"},
            {"2", "ABPL", "B", "5", "100"},
            {"3", "AAPL", "S", "2", "80"},
            {"4", "ABPL", "S", "2", "120"},
            // need to sell multiple stocks
            {"5", "GOOG", "B", "10", "80"}
    };
    getUserPortfolioWithMarginCall(records, portfolio);
    cout << "\nQ2 test case 4: ";
    print(portfolio);
    
    records = {
            {"1", "AAPL", "B", "5", "100"}, 
            {"2", "GOOG", "B", "5", "75"},
            {"3", "AAPLO", "B", "5", "50"}
    };
    getUserPortfolioWithCollateral(records, portfolio);
    cout << "\nQ3 test case 0: ";
    print(portfolio);

    records = {
            {"1", "AAPL", "B", "6", "50"}, 
            {"2", "GOOG", "B", "6", "50"},
            {"3", "AAPLO", "B", "5", "25"},
            {"4", "GOOG0", "B", "5", "25"},
            {"5", "TEST", "B", "250", "1"}
        
    };
    getUserPortfolioWithCollateral(records, portfolio);
    cout << "\nQ3 test case 1: ";
    print(portfolio);  
}
"""