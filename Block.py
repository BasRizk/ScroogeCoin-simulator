class Block:
    
    _current_id = 0
    _capacity = 10
    
    def __init__(self, prev_hash_pt):
        self.id = self._current_id
        self.prev_hash_pt = prev_hash_pt
        self.transactions = []
        self.hash = None

        Block._current_id += 1
    
    def add_transaction(self, trans):
        self.transactions.append(trans)
        if len(self.transactions) >= self._capacity:
            return True
        return False

    def get_print_mini(self):
            transactions = ''
            for transaction in self.transactions:
                transactions += str(transaction.id) + ','
            return 'Block:\t' + str(self.id) + '\n'\
                    + 'Previous:\t' + ((str(self.prev_hash_pt[0].id) + ', ' + str(self.prev_hash_pt[1])) if self.prev_hash_pt else 'None') + '\n'\
                    + 'Transactions:\t{ ' + transactions[:-1] + ' }\n'\
                    + 'Hash:\t' + str(self.hash) + '\n'
    def get_print(self):
        transactions = ''
        for transaction in self.transactions[:-1]:
            transactions += transaction.get_print_mini() + '--------\n'
        if len(self.transactions):
            transactions += self.transactions[-1].get_print()
        return 'Block:\t' + str(self.id) + '\n'\
                + 'Previous:\t' + ((str(self.prev_hash_pt[0].id) + ', ' + str(self.prev_hash_pt[1])) if self.prev_hash_pt else 'None') + '\n'\
                + 'Transactions: {\n' + transactions + '}\n'\
                + 'Hash:\t' + str(self.hash) + '\n'
                
    def __str__(self):
        transactions = ''
        for transaction in self.transactions:
            transactions += '\t' + transaction.get_print() + '--------\n'
        return 'Block:\t' + str(self.id) + '\n'\
                + 'Previous:\t' + ((str(self.prev_hash_pt[0].id) + ', ' + str(self.prev_hash_pt[1])) if self.prev_hash_pt else 'None') + '\n'\
                + 'Transactions: {\n' + transactions + '}\n'