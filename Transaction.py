class Transaction:

    _current_id = 0
        
    
    def __new__(cls, sender, amount, recipient_vk): 
        print("Creating Transaction") 
        # Create transaction only if coins available 
        coins = sender.get_coins(amount)
        if (coins is not None) & (len(coins) == amount):            
            return super(Transaction, cls).__new__(cls) 
        else:
            return None
     
    def __init__(self, sender, amount, recipient_vk):
        self.id = _current_id
        self.sender = sender
        self.amount = amount
        self.recipient_vk = recipient_vk
        self.prev_hash_pt = None
        self.hash = None
        self.signature = None
        # Already verified
        self.coins = sender.get_coins(amount, spend=True)
        _current_id += 1

    def __str__(self):
        return 'Transaction:\t' + str(self.id) + '\n'\
                + 'Previous:\t' + str(self.prev_hash_pt[0].id) + ', ' + str(self.prev_hash_pt[1]) + '\n'\
                + 'Amount:\t' + str(self.amount) + '\n'\
                + 'From:\t' + str(self.sender.vk) + '\n'\
                + 'To:\t' + str(self.recipient_vk)
    
    
