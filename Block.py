from hashlib import sha256
from base64 import b64encode

class Block:
    
    id = 0
    capacity = 10
    
    def __init__(self, _prev_hash_pt):
        self.id = id
        self.prev_hash_pt = prev_hash_pt
        self.transactions = []
        self.hash = ''

        id += 1
    
    def add_transaction(self, trans):
        self._transactions.append(trans)
        if len(self.transactions) >= capacity:
            return True
        return False