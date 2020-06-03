from Ledger import Ledger

class Transaction:

    _current_id = 0
        
    def __new__(cls, sender_vk, amount, recipient_vk, coins=None): 
        # Create transaction only if enough coins available 
        coins = Ledger.get_coins(sender_vk, amount) if coins is None else coins
        if (coins is not None) & (len(coins) == amount):            
            return super(Transaction, cls).__new__(cls) 
        else:
            return None
     
    def __init__(self, sender_vk, amount, recipient_vk, coins=None):
        self.id = self._current_id
        self.sender_vk = sender_vk
        self.amount = amount
        self.recipient_vk = recipient_vk
        self.prev_hash_pt = None
        self.hash = None
        self.signature = None
        self.coins = Ledger.get_coins(sender_vk, amount) if coins is None else coins
        Transaction._current_id += 1

    def _prev_hash_pt_str(self):
        _prev_str = "Previous:\n\t{"
        if self.prev_hash_pt is not None:
            for pt in self.prev_hash_pt:
                _prev_str +=\
                    '\t\t' + str(pt[0].id) \
                     + ', ' + str(pt[1]) \
                     + '\n'
        _prev_str += '\n\t}'
        return _prev_str
    
    def get_print_mini(self):
        coins = ''
        for coin in self.coins:
            coins += str(coin._id) + ','
        return '\tTransaction:\t' + str(self.id) + '\n'\
                    + self._prev_hash_pt_str() + '\n'\
                    + '\tAmount:\t' + str(self.amount) + '\n'\
                    + '\tCoins:\t{ ' + coins[:-1] + ' }\n'\
                    + '\tFrom:\t' + str(self.sender_vk) + '\n'\
                    + '\tTo:\t' + str(self.recipient_vk) + '\n'\
                    + '\tSignature:\t' + str(self.signature) + '\n'\
                    + '\tHash:\t' + str(self.hash) + '\n'
    def get_print(self):
        coins = ''
        for coin in self.coins:
            coins += '\t' + str(coin._id) + ': ' + str(coin._signature) + '\n\t--------\n'
    
        return '\tTransaction:\t' + str(self.id) + '\n'\
                    + self._prev_hash_pt_str() + '\n'\
                    + '\tAmount:\t' + str(self.amount) + '\n'\
                    + '\tCoins:{\n' + coins + '\t}\n'\
                    + '\tFrom:\t' + str(self.sender_vk) + '\n'\
                    + '\tTo:\t' + str(self.recipient_vk) + '\n'\
                    + '\tSignature:\t' + str(self.signature) + '\n'\
                    + '\tHash:\t' + str(self.hash) + '\n'

    def __str__(self):
        coins = ''
        for coin in self.coins:
            coins += str(coin._id) + ': ' + str(coin._signature) + '\n--------\n'
            
        return 'Transaction:\t' + str(self.id) + '\n'\
                + self._prev_hash_pt_str() + '\n'\
                + 'Amount:\t' + str(self.amount) + '\n'\
                + 'Coins:{\n' + coins + '}\n'\
                + 'From:\t' + str(self.sender_vk) + '\n'\
                + 'To:\t' + str(self.recipient_vk) + '\n'
                
    def has_coin(self, coin):
        if coin in self.coins:
            return True
        return False