from hashlib import sha256
from ecdsa import SigningKey

import Transaction
import Ledger

class User:
    
    def __init__(self):
        self.coins = []
        self._sk = SigningKey.generate()
        self.vk = self._sk.verifying_key
        Ledger.add_user(self.vk)

    def pay(self, amount, recipient_vk):
        transaction = Transaction(self, amount, recipient_vk)
        if transaction is not None:
            transaction.signature = self._sk.sign(str(transaction))
            transaction.hash = sha256(str(transaction)+(transaction.signature)
                                  .encode('utf-8')).hexdigest()
            return transaction
        print("Not enough coins available")
        return None