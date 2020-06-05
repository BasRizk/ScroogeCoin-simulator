from hashlib import sha256
from ecdsa import SigningKey, NIST384p

from Transaction import Transaction
from Ledger import Ledger

import logging

class User:

    _current_id = 0
    
    def __init__(self):
        self._id = self._current_id
        self._sk = SigningKey.generate(curve=NIST384p, hashfunc=sha256)
        self.vk = self._sk.verifying_key.to_string().hex()
        Ledger.add_user(self.vk)
        User._current_id += 1

    def pay(self, amount, recipient_vk, coins=None):
        transaction = Transaction(self.vk, amount, recipient_vk, coins)
        if transaction is not None:
            transaction.signature = self._sk.sign(str(transaction).encode('utf-8')).hex()
            transaction.hash = sha256((str(transaction) + str(transaction.signature)).encode('utf-8')).hexdigest()
            logging.info("User side :: Issued a transaction with id %d" % transaction.id)
            Ledger.register_transaction(transaction)
            return transaction
        logging.error("User side :: Not enough coins available")
        return None
    
    def get_balance(self):
        return Ledger.get_coins(self.vk)
    
# =============================================================================
# --------- For acting as a recipient    
# =============================================================================
    def get_incoming_transactions(self):
        return Ledger.get_incoming_transactions(self.vk)
    
    def confirm_incoming_transaction(self, transaction, verify=True, verbose=True):
        # TODO maybe update balance at user-end accordingly
        if verbose:
            logging.info("Recipient side :: about to confirm an incoming transaction..")
        if verify and Ledger.verify_transaction_existance(transaction, verbose):
            Ledger.confirm_transaction(transaction)
            logging.info("Recipient side :: User #%d accepted transaction with id %d; verification succeded.\n" % (self._id,transaction.id))
            return True
        elif verify:
            if verbose:
                logging.info("Recipient side :: not accepting incoming transaction; verification failed.\n" )
            return False
        else:
            if verbose:
                logging.info("Recipient side :: accepted incoming transaction without confirmation\n")
            Ledger.confirm_transaction(transaction)
            
            return True
