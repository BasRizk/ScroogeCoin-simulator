class Ledger:

    def __init__(self):
        self.blockchain = []
        self.last_hp = None
        self.last_hp_signed = ''

    def add_block(self, block):
        self.blockchain.append(block)
