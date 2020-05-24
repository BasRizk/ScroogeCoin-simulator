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
from ecdsa import SigningKey

import Ledger
import Transaction
import Coin
import Block

class Scrooge:
    
    def __init__(self):
        self.ledger = Ledger()
        self._current_block = Block(None)
        self._current_id = 0
        self._coins = []
        self._last_transaction_hash_pt = None
        
        # Keys
        self._sk = SigningKey.generate()
        self.vk = self._sk.verifying_key

    def run(self):
        pass

    def publish_block(self):
        self._current_block.hash = sha256(self._current_block.encode('utf-8')).hexdigest()        
        self.ledger.add_block(self._current_block)
        
        self._current_block = Block((self._current_block, self._current_block.hash))

        self.ledger.last_hash_pt = self._current_block.prev_hash_pt
        self.ledger.last_hash_pt_signed = self.sk.sign(self.ledger.last_hash_pt)

    def publish_transaction(self, transaction):
        # Publish transaction to the block
        transaction.prev_hash_pt = self._last_transaction_hash_pt
        is_full = self._current_block.add_transaction(transaction)
        # TO-REVISE
        self._last_transaction_hash_pt = (transaction, transaction.hash)
        if is_full:
            self.publish_block()
    

    def verify_owner(self, transaction):
        # Verify that the transaction belongs to the owner
        return transaction.sender.vk.verify(transaction.signature, str(transaction))

    def verify_no_double_spending(self, transaction):
        # Verify that the transaction is not a Double spending
        for c_loop in transaction.coins:
            t_loop = self._last_transaction_hash_pt[0]
            while True:
                if c_loop in t_loop.coins:
                    if transaction.sender.vk != t_loop.recipient_vk:
                        return False
                    break
                t_loop = t_loop.prev_hash_pt[0]
        return True
    
# TO-REVISE IS LAST_HASH_PT PUBLIC OR NOT
# IF SOME ONE ADDED SOMETHING TO LEDGER
# 

    def handle_payment_transaction(self, transaction):
        if self.verify_owner(transaction) and self.verify_double_spending(transaction):
            self.publish_transaction(transaction)
            return True
        return False
    
    def create_coin_transaction(self, recipient_vk, amount):
        coin = self.create_coin()
        
        transaction = Transaction(vk, amount, recipient_vk)
        transaction.signature = self.sk.sign(str(transaction))
        transaction.hash = sha256(str(transaction)+(transaction.signature).encode('utf-8')).hexdigest()

        self.publish_transaction(transaction)


    def create_coin(self):
        # Generate unique coin id
        # Sign by scrooge
        c = Coin(self._current_id)
        c.sign(self.sk.sign(str(c)))
        self._current_id += 1
        self._coins.append(c) 
        
        