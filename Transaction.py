class Transaction:

    _current_id = 0
        
    def __init__(self, sender, amount, recipient_vk):
        self.id = _current_id
        self.sender = sender
        self.amount = amount
        self.recipient_vk = recipient_vk
        self.prev_hash_pt = ''
        self.hash = ''
        self.signature = ''
        # TODO
        self.coins = sender.get_coins(amount)

        _current_id += 1

    def __str__(self):
        return str(self.id) + self.prev_hash_pt + str(self.amount) + self.recipient
    
    
    # TODO Create coins after get_coins 