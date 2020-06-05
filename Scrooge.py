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

import random
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
        # self._last_transaction_hash_pt = None
        self._processed_nonconfirmed_transactions = []
        logging.debug("Scrooge :: I just woke up! ... scrooge initialized.")

        
    def publish_block(self):
        self._current_block.hash = sha256(str(self._current_block).encode('utf-8')).hexdigest() 
        
        # Upon that command block transactions are executed
        # self._ledger.add_block(self._current_block)
        
        # Apply Block Transactions (Exchange Coins)
        for t in self._current_block.transactions:
            consumed_coins = t.coins
            sender_coins = self._ledger._users_coins[t.sender_vk]
            left_over_coins =\
                [c for c in sender_coins if c not in consumed_coins]
            self._ledger._users_coins[t.sender_vk] = left_over_coins
            random.shuffle(self._ledger._users_coins[t.sender_vk])
            self._ledger._users_coins[t.recipient_vk] =\
                self._ledger._users_coins[t.recipient_vk] + consumed_coins
            random.shuffle(self._ledger._users_coins[t.recipient_vk])
            
        transactions_hashes = [t.hash for t in self._current_block.transactions]
        self._ledger._merkle_tree.extend(transactions_hashes)

        self._current_block = Block((self._current_block, self._current_block.hash))

        self._ledger._last_hash_pt = self._current_block.prev_hash_pt
        self._ledger._last_hash_pt_signed = self._sk.sign((str(self._ledger._last_hash_pt[0]) + str(self._ledger._last_hash_pt[1])).encode('utf-8'))
        logging.info("Scrooge :: A Block is published, and merkle tree extended.")
        logging.info(str(self._ledger))



    def publish_transaction(self, transaction):
        # Publish transaction to the block
        # transaction.prev_hash_pt = self._last_transaction_hash_pt
        transaction.hash = sha256((str(transaction) + str(transaction.signature)).encode('utf-8')).hexdigest()
        
        is_full = self._current_block.add_transaction(transaction)

        # self._last_transaction_hash_pt = (transaction, transaction.hash)
        logging.debug("Scrooge :: transaction id %d was added to current block as #%d." %
                      (transaction.id, len(self._current_block.transactions)))

        logging.info(self._current_block.get_print())
    
        if is_full:
            logging.debug("Scrooge :: a block is full, about to be published then..")
            self.publish_block()
# =============================================================================
#             Verifications
# =============================================================================
    def get_coin_recent_usage(self, coin):
        # Check in current block first
        for t in self._current_block.transactions:
            if coin in t.coins:
                return t
        # Otherwise search from published ones
        return self._ledger.get_coin_recent_usage(coin)
    
    def verify_coins_are_real(self, transaction):
        # WHILE ADDING HASH PTS OF PREV COINS USAGE
        # Verify that coins are real
        prev_hash_pts = []
        for coin in transaction.coins:
            prev_transaction = self.get_coin_recent_usage(coin)
            if prev_transaction is None:
                logging.info("Scrooge :: Verification failed: Coin does not exist in history probably. Ignore Transaction.")
                return False
            prev_hash_pts.append((prev_transaction, prev_transaction.hash))
        transaction.prev_hash_pt = prev_hash_pts
        logging.info("Scrooge :: Coins are real verified")
        return True
        
    def verify_owner(self, transaction):
        # Verify that the transaction belongs to the owner
        try:
            if VerifyingKey.from_string(bytes.fromhex(transaction.sender_vk), curve=NIST384p)\
                .verify(bytes.fromhex(transaction.signature), str(transaction).encode('utf-8'), sha256):
                    logging.info("Scrooge :: owner of transaction verified.")
                    return True
        except BadSignatureError:
            pass
        logging.info("Scrooge :: Verification failed: sender is not the issuer of signature. Ignore Transaction.")
        return False
    
    def verify_no_double_spending(self, transaction):
        # Verify that the transaction is not a Double spending
        
        # logging.debug("--------------look up---------")
        # logging.debug(transaction.prev_hash_pt)
        for c, pt in zip(transaction.coins, transaction.prev_hash_pt):
            prev_transaction, _ = pt
            proof = self._ledger._merkle_tree.get_proof(prev_transaction.hash)
            
            if not c in prev_transaction.coins:
                logging.error("Scrooge :: Verification failed: coin ptr not found")

            if (not self._ledger._merkle_tree.verify_leaf_inclusion(prev_transaction.hash, proof)) and \
                  (not prev_transaction in self._current_block.transactions):
                logging.error("Scrooge :: Verification failed: Coin does not exist in history probably")
                return False
            
            if transaction.sender_vk != prev_transaction.recipient_vk:
                logging.info("Scrooge :: Verification failed: Double spending attack detected. Ignore Transaction.")
                logging.info(transaction.get_print())
                return False
        
        logging.info("Scrooge :: No double spending verified.")
        return True

    def handle_next_transaction(self):
        logging.debug("Scrooge :: about to handle a transaction.")
        while(True):
            transaction = self._ledger._unconfirmed_transactions.pop(0)
            if not transaction in self._processed_nonconfirmed_transactions:
                break
            self._ledger._unconfirmed_transactions.append(transaction)
        logging.debug("Scrooge :: handle transaction with id %d." % transaction.id)
    # def handle_payment_transaction(self, transaction):
        if self.verify_owner(transaction) and\
            self.verify_coins_are_real(transaction) and\
            self.verify_no_double_spending(transaction):
            self.publish_transaction(transaction)
            self._ledger._unconfirmed_transactions.append(transaction)
            self._processed_nonconfirmed_transactions.append(transaction)
            return True
        return False
    
    def create_coin_transaction(self, recipient_vk, amount):
        for i in range(amount):
            self.create_coin()
        transaction = Transaction(self.vk, amount, recipient_vk, self._coins)
        self._coins = []
        transaction.signature = self._sk.sign(str(transaction).encode('utf-8')).hex()
        logging.info("Scrooge :: created a coin transaction of id %d with an amount of %d" % (transaction.id, amount))
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
        