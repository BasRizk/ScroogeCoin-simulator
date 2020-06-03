class Coin:
    
    def __init__(self, _id):
        self._id = _id
        self._signature = None
        
    def sign(self, signature):
        self._signature = signature.hex()

    def __eq__(self, other):
        # Note: generally, floats should not be compared directly
        # due to floating-point precision
        return (self._id == other._id) and (self._signature == other._signature)