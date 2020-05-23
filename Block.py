from hashutils import hash_sha256
from base64 import b64encode

class Block:
    def __init__(self, _id, _transactions, _hash, _prev_hash_pt):
        self._id = _id
        self._transactions = []
        self._hash = _hash
        self._prev_hash_pt = _prev_hash_pt 
    
    def add_transaction(self, trans):
        self._transactions.append(trans)