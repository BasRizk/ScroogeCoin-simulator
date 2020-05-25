class Ledger:
    
    __instance = None
    
    def __new__(cls, scrooge_vk):
        if Ledger.__instance is None:
            Ledger.__instance = object.__new__(cls)
            Ledger.__instance._sealed = False
        return Ledger.__instance

    def __init__(self, scrooge_vk=None):
        if self._sealed:
            return
        self._sealed = True

        self.last_hash_pt = None
        self.last_hash_pt_signed = None
        
        self._users_coins = {}
        self._users_coins[scrooge_vk] = []
        

    def __str__(self):
        block = self.last_hash_pt[0]
        blockchain = ''
        while True:
            blockchain += (str(block) + '\n')
            block = block.prev_hash_pt[0]
        return blockchain
    
    def add_block(self, block):
        # Apply Block Transactions (Exchange Coins)
        for t in block.transactions:
            consumed_coins = t.coins
            sender_coins = self._user_coins[t.sender_vk]
            left_over_coins =\
                [c for c in sender_coins if c not in consumed_coins]
            self._users_coins[t.sender_vk] = left_over_coins
            self._users_coins[t.recipient_vk].append(consumed_coins)
        
    @staticmethod       
    def get_coins(user_vk, amount):
        if Ledger.__instance is None:
            return None
        available_coins = Ledger.__instance._users_coins[user_vk]
        if len(available_coins) < amount:
            return None
        to_spend_coins = Ledger.__instance.coins[:amount]
        return to_spend_coins
    
    @staticmethod
    def add_user(user_vk):
        if Ledger.__instance is None:
            return None
        Ledger.__instance._users_coins[user_vk] = []

    @staticmethod
    def view_users():
        if Ledger.__instance is None:
            return None
        return Ledger.__instance._users_coins.copy()
    
        