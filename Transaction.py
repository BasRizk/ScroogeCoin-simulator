from Crypto.PublicKey import RSA

class Transaction:
    def __init__(self, _id, _prev_hash_pt, _amount, _signature):
        self._id = _id
        self._prev_hash_pt = _prev_hash_pt
        self._amount = _amount
        self._signature = _signature