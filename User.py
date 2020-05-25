from hashlib import sha256
from ecdsa import SigningKey

import Transaction

class User:
    # TO-REVISE how to access public keys
    def __init__(self):
        self.coins = []
        self._sk = SigningKey.generate()
        self.vk = self._sk.verifying_key

    def pay(self, amount, recipient_vk):
        transaction = Transaction(self, amount, recipient_vk)
        if transaction is not None:
            # TODO what to do with it now
            pass
        # TODO Notify user

    def sign(self, content):
        return self._sk.sign(content)
    
    def confirm_transaction(self, transaction):
        pass
    
    def get_coins(self, amount, spend=False):
        if len(self.coins) < amount:
            return None

        self.coins.shuffle()
        to_spend_coins = self.coins[:amount]
        if spend:
            coins = coins[amount:]
        return to_spend_coins