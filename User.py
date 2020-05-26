from hashlib import sha256
from ecdsa import SigningKey, VerifyingKey, NIST384p

from Transaction import Transaction
from Ledger import Ledger

class User:
    
    def __init__(self):
        self.coins = []
        self._sk = SigningKey.generate(curve=NIST384p, hashfunc=sha256)
        self.vk = self._sk.verifying_key.to_string().hex()
        Ledger.add_user(self.vk)

    def pay(self, amount, recipient_vk):
        transaction = Transaction(self.vk, amount, recipient_vk)
        if transaction is not None:
            transaction.signature = self._sk.sign(str(transaction).encode('utf-8')).hex()
            transaction.hash = sha256((str(transaction) + str(transaction.signature)).encode('utf-8')).hexdigest()
            return transaction
        print("Not enough coins available")
        return None