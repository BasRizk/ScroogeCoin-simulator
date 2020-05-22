from hashutils import hash_sha256
from base64 import b64encode
from Crypto.PublicKey import RSA

class Scrooge:
    def __init__(self, ledger):
        self.ledger = ledger

    def verify_owner(self):
        # Verify that the transaction belongs to the owner
        pass
    def verify_double_spending(self):
        # Verify that the transaction is not a Double spending
        pass
    
    def publish_transaction(self):
        # Publish transaction to the block
        pass