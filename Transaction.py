from Crypto.PublicKey import RSA

class Transaction:
        
    def __init__(self, _id, _hash, _prev_hash_pt, _amount, _signature):
        self._id = _id
        self._hash = self.generate_hash()
        self._prev_hash_pt = _prev_hash_pt
        self._amount = _amount
        self._signature = _signature
        
    def generate_hash(self):
        pass
    