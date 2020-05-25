class Block:
    
    _current_id = 0
    _capacity = 10
    
    def __init__(self, prev_hash_pt):
        self.id = self._current_id
        self.prev_hash_pt = prev_hash_pt
        self.transactions = []
        self.hash = None

        self._current_id += 1
    
    def add_transaction(self, trans):
        self._transactions.append(trans)
        if len(self.transactions) >= self._capacity:
            return True
        return False

    def __str__(self):
        return 'Block:\t' + str(self.id) + '\n'\
                + 'Previous:\t' + str(self.prev_hash_pt[0].id) + ', ' + str(self.prev_hash_pt[1]) + '\n'\
                + 'Transactions:\t' + str(self.transactions) + '\n'\
                + 'Hash:\t' + str(self.hash) + '\n'