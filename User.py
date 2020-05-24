from hashlib import sha256
from ecdsa import SigningKey

import Transaction

class User:
    
    def __init__(self):
        self.coins = []
        self._sk = SigningKey.generate()
        self.vk = _sk.verifying_key

    def pay(self, amount, recipient_vk):
        transaction = Transaction(self, amount, recipient_vk)

    def confirm_transaction(self, transaction):
        pass