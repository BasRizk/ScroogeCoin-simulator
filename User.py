from hashlib import sha256

class User:
    
    def __init__(self, _signature):
        self._signature = _signature

    def pay(self, amount, another_user):
        pass
    
    def confirm_transaction(self, transaction):
        pass