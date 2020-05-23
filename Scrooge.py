"""
❖ A designated entity “Scrooge” publishes an append-only ledger that
contains all the history of transactions.

❖ The ledger is a blockchain, where each block contains transactions,
its ID, the hash of the block, and a hash pointer to the previous block.
The final hash pointer is signed by Scrooge.

❖ The design and implementation of the ledger based on the concept of
the blockchain (hash linked list).

❖ Upon detecting any transaction, scrooge verifies it by making sure the
coin really belongs to the owner and it has not been spent before.
❖ If verified, Scrooge adds the transaction to the blockchain. Double
spending can only happen before the transaction is published.

"""
from hashlib import sha256
from base64 import b64encode
from Crypto.PublicKey import RSA

class Scrooge:
    
    def __init__(self):
        self.ledger = []
        self._current_id = 0
        self._coins = []

    def run(self):
        pass

    def verify_owner(self):
        # Verify that the transaction belongs to the owner
        pass
    def verify_double_spending(self):
        # Verify that the transaction is not a Double spending
        pass
    
    def publish_transaction(self):
        # Publish transaction to the block
        pass
    
    def create_coin(self):
        # Generate unique coin id
        # Sign by goofy
        Coin c = Coin(self._current_id)
        c.sign(sign)
        self._current_id += 1
        self._coins.append(c)
        
        