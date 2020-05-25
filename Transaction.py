import Ledger

class Transaction:

    _current_id = 0
        
    # TODO GET LEDGER
    def __new__(cls, sender_vk, amount, recipient_vk): 
        print("Creating Transaction") 
        # Create transaction only if enough coins available 
        coins = Ledger.get_coins(sender_vk, amount)
        if (coins is not None) & (len(coins) == amount):            
            return super(Transaction, cls).__new__(cls) 
        else:
            return None
     
    def __init__(self, sender_vk, amount, recipient_vk):
        self.id = self._current_id
        self.sender_vk = sender_vk
        self.amount = amount
        self.recipient_vk = recipient_vk
        self.prev_hash_pt = None
        self.hash = None
        self.signature = None
        self.coins = Ledger.get_coins(sender_vk, amount)
        self._current_id += 1

    def __str__(self):
        return 'Transaction:\t' + str(self.id) + '\n'\
                + 'Previous:\t' + str(self.prev_hash_pt[0].id) + ', ' + str(self.prev_hash_pt[1]) + '\n'\
                + 'Amount:\t' + str(self.amount) + '\n'\
                + 'From:\t' + str(self.sender_vk) + '\n'\
                + 'To:\t' + str(self.recipient_vk)
    
    
