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
from ecdsa import SigningKey, VerifyingKey, NIST384p, BadSignatureError

from Ledger import Ledger
from Transaction import Transaction
from Coin import Coin
from Block import Block

import logging

class Scrooge:
         
    __instance = None
    def __new__(cls):
        if Scrooge.__instance is None:
            Scrooge.__instance = object.__new__(cls)
            Scrooge.__instance._sealed = False
        return Scrooge.__instance
    
    def __init__(self):
        if self._sealed:
            return
        
        self._sealed = True
        # Keys
        self._sk = SigningKey.generate(curve=NIST384p, hashfunc=sha256)
        self.vk = self._sk.verifying_key.to_string().hex()
        
        self._ledger = Ledger(self.vk)
        self._current_block = Block(None)
        self._current_id = 0
        self._coins = []
        self._last_transaction_hash_pt = None
        
    def publish_block(self):
        self._current_block.hash = sha256(str(self._current_block).encode('utf-8')).hexdigest() 
        
        # Upon that command block transactions are executed
        # self._ledger.add_block(self._current_block)
        
        # Apply Block Transactions (Exchange Coins)
        for t in block.transactions:
            consumed_coins = t.coins
            sender_coins = self._ledger._users_coins[t.sender_vk]
            left_over_coins =\
                [c for c in sender_coins if c not in consumed_coins]
            self._ledger._users_coins[t.sender_vk] = left_over_coins
            random.shuffle(self._ledger._users_coins[t.sender_vk])
            self._ledger._users_coins[t.recipient_vk] =\
                self._ledger._users_coins[t.recipient_vk] + consumed_coins
            random.shuffle(self._ledger._users_coins[t.recipient_vk])
        self._ledger._merkle_tree.extend(block.transactions)
        logging.info("A Block is published")
        
        self._current_block = Block((self._current_block, self._current_block.hash))

        self._ledger.last_hash_pt = self._current_block.prev_hash_pt
        self._ledger.last_hash_pt_signed = self._sk.sign((str(self._ledger.last_hash_pt[0]) + str(self._ledger.last_hash_pt[1])).encode('utf-8'))
        logging.info(str(self._ledger))

    def publish_transaction(self, transaction):
        # Publish transaction to the block
        transaction.prev_hash_pt = self._last_transaction_hash_pt
        transaction.hash = sha256((str(transaction) + str(transaction.signature)).encode('utf-8')).hexdigest()
        is_full = self._current_block.add_transaction(transaction)

        self._last_transaction_hash_pt = (transaction, transaction.hash)
        
        logging.info(self._current_block.get_print())

        if is_full:
            self.publish_block()
        

    def verify_owner(self, transaction):
        # Verify that the transaction belongs to the owner
        try:
            return VerifyingKey.from_string(bytes.fromhex(transaction.sender_vk), curve=NIST384p).verify(bytes.fromhex(transaction.signature), str(transaction).encode('utf-8'), sha256)
        except BadSignatureError:
            logging.info("Verification failed")
        return False
    def verify_no_double_spending(self, transaction):
        # Verify that the transaction is not a Double spending
        for c_loop in transaction.coins:
            t_loop = self._last_transaction_hash_pt[0]
            while True:
                if c_loop in t_loop.coins:
                    if transaction.sender_vk != t_loop.recipient_vk:
                        logging.info("Double spending attack detected. Ignore Transaction.")
                        logging.info(transaction.get_print())
                        return False
                    break
                t_loop = t_loop.prev_hash_pt[0]
                if t_loop is None:
                    logging.info("Double spending attack detected. Ignore Transaction.")
                    logging.info(transaction.get_print())
                    return False
        return True

    def handle_payment_transaction(self, transaction):
        if self.verify_owner(transaction) and self.verify_no_double_spending(transaction):
            self.publish_transaction(transaction)
            return True
        return False
    
    def create_coin_transaction(self, recipient_vk, amount):
        for i in range(amount):
            self.create_coin()
        transaction = Transaction(self.vk, amount, recipient_vk, self._coins)
        self._coins = []
        transaction.signature = self._sk.sign(str(transaction).encode('utf-8')).hex()
        self.publish_transaction(transaction)


    def create_coin(self):
        # Generate unique coin id
        c = Coin(self._current_id)
        # Sign by scrooge
        c.sign(self._sk.sign(str(c).encode('utf-8')))
        self._current_id += 1
        self._coins.append(c)
        # Add coin to block chain, as owned by Scrooge user
        self._ledger._users_coins[self.vk].append(c)
        
        