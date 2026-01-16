"""
Social App: Friends + Money Transfers
You are given a list of API requests. Each request is:[seqId, path]
seqId is a unique string like "1", "2", ...
path is one of these:

1) Register
v1/REGISTER/{user}/{initialBalance}
Create a new user with starting balance.

2) Send friend request
v1/FRIEND_REQUEST/{fromUser}/{toUser}
Create a pending friend request.
Store it using this request’s seqId.

3) Accept friend request
v1/ACCEPT_FRIEND/{seqId}
Accept the earlier friend request whose sequence id is seqId.
After acceptance, the two users become friends forever (undirected).

4) Send money
v1/SEND_MONEY/{fromUser}/{toUser}/{amount}
Transfer amount from fromUser to toUser only if:
they are already friends, and
fromUser has at least amount balance
Otherwise, ignore this request.

Task
Process requests in order and return final balances of all users as strings:
"user:balance"
Order of output does not matter.
"""

from collections import defaultdict
from typing import Dict, List, Set, Tuple

def finalBalances(requests):
    balance: Dict[str, int] = {}
    friends: Dict[str, Set[str]] = defaultdict(set) # undirected
    pending: Dict[str, Tuple[str, str]] = {} # seqId -> (fromUser, toUser)

    for seqId, path in requests:
        parts = path.split('/')
        action = parts[1]

        if action == 'REGISTER':
            user = parts[2]
            balance[user] = int(parts[3])
        
        elif action == 'FRIEND_REQUEST':
            fromUser, toUser = parts[2], parts[3]
            pending[seqId] = (fromUser, toUser)
        
        elif action == 'ACCEPT_FRIEND':
            reqId = parts[2]
            if reqId in pending:
                a, b = pending.pop(reqId)
                friends[a].add(b)
                friends[b].add(a)
        
        else:
            fromUser, toUser, amount = parts[2], parts[3], int(parts[-1])

            if toUser in friends[fromUser] and balance.get(fromUser, 0) >= amount:
                balance[fromUser] -= amount
                balance[toUser] = balance.get(toUser, 0) + amount
    # time O(r) r is length of request
    # space O(U + F + P) user count + friendship count + pending count
    return [f'{user}:{bal}' for user, bal in balance.items()]

# T1: sample 1 (friendship required)
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/REGISTER/Charlie/75"],
    ["4", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["5", "v1/ACCEPT_FRIEND/4"],
    ["6", "v1/SEND_MONEY/Alice/Bob/30"],
    ["7", "v1/SEND_MONEY/Charlie/Alice/25"],  # not friends -> ignored
]
expected = sorted(["Alice:70", "Bob:80", "Charlie:75"])
assert sorted(finalBalances(requests)) == expected


# T2: sample 2 (two-way transfers after being friends)
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/REGISTER/Charlie/75"],
    ["4", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["5", "v1/ACCEPT_FRIEND/4"],
    ["6", "v1/SEND_MONEY/Alice/Bob/20"],
    ["7", "v1/SEND_MONEY/Bob/Alice/10"],
]
expected = sorted(["Alice:90", "Bob:60", "Charlie:75"])
assert sorted(finalBalances(requests)) == expected


# T3: sample 3 (send money without friendship -> ignored)
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/SEND_MONEY/Alice/Bob/30"],  # not friends -> ignored
]
expected = sorted(["Alice:100", "Bob:50"])
assert sorted(finalBalances(requests)) == expected


# T4: insufficient balance -> ignored
requests = [
    ["1", "v1/REGISTER/Alice/10"],
    ["2", "v1/REGISTER/Bob/0"],
    ["3", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["4", "v1/ACCEPT_FRIEND/3"],
    ["5", "v1/SEND_MONEY/Alice/Bob/20"],  # Alice has only 10 -> ignored
]
expected = sorted(["Alice:10", "Bob:0"])
assert sorted(finalBalances(requests)) == expected


# T5: accept unknown friend request id -> ignored
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/100"],
    ["3", "v1/ACCEPT_FRIEND/999"],        # no such pending request
    ["4", "v1/SEND_MONEY/Alice/Bob/10"],  # still not friends -> ignored
]
expected = sorted(["Alice:100", "Bob:100"])
assert sorted(finalBalances(requests)) == expected


# T6: two pending requests, accept only one
requests = [
    ["1", "v1/REGISTER/Alice/100"],
    ["2", "v1/REGISTER/Bob/50"],
    ["3", "v1/REGISTER/Charlie/70"],
    ["4", "v1/FRIEND_REQUEST/Alice/Bob"],
    ["5", "v1/FRIEND_REQUEST/Alice/Charlie"],
    ["6", "v1/ACCEPT_FRIEND/4"],          # Alice-Bob become friends
    ["7", "v1/SEND_MONEY/Alice/Bob/30"],  # succeeds
    ["8", "v1/SEND_MONEY/Alice/Charlie/30"], # not friends yet -> ignored
]
expected = sorted(["Alice:70", "Bob:80", "Charlie:70"])
assert sorted(finalBalances(requests)) == expected
