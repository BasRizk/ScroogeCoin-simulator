class Coin:
    
    def __init__(self, _id):
        self._id = _id
        self._signature = None
        
    def sign(self, signature):
        self._signature = signature
