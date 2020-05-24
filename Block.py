from hashlib import sha256
from base64 import b64encode

class Block:
    
    _current_id = 0
    _capacity = 10
    
    def __init__(self, prev_hash_pt):
        self.id = current_id
        self.prev_hash_pt = prev_hash_pt
        self.transactions = []
        self.hash = None

        _current_id += 1
    
    def add_transaction(self, trans):
        self._transactions.append(trans)
        if len(self.transactions) >= _capacity:
            return True
        return False
    