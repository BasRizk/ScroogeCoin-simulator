import logging

from merklelib import MerkleTree, beautify

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

        self._last_hash_pt = None
        self._last_hash_pt_signed = None
        
        self._users_coins = {}
        self._users_coins[scrooge_vk] = []
        self._merkle_tree = MerkleTree()
        self._unconfirmed_transactions = []

    def __str__(self):
        block = self._last_hash_pt[0] if self._last_hash_pt else None
        blockchain = '\n'
        while True:
            if block is None:
                break
            blockchain += (block.get_print_mini() + '\n---------------------------------\n')
            block = block.prev_hash_pt[0] if block.prev_hash_pt else None
        blockchain += "\n--------------------------------\n\tWallets\n--------------------------------\n"
        for vk, coins in self._users_coins.items():
            blockchain += vk + ':\n' + str(len(coins))
            blockchain += '\n--------------------------------\n'
        return blockchain
    
    def get_coin_recent_usage(self, coin):
        
        current_hash_pt = self._last_hash_pt
        while(True):
            if current_hash_pt is None:
                break
            current_block, _  = current_hash_pt
            
            for t in current_block.transactions:
                if t.has_coin(coin):
                    return t
                
            current_hash_pt = current_block.prev_hash_pt
            
        return None
            
    @staticmethod
    def register_transaction(transaction):
        if Ledger.__instance is None:
            logging.error("No Ledger is created")
            return None
        Ledger.__instance._unconfirmed_transactions.append(transaction)
        logging.info("Ledger :: Transaction is registered in the Ledger; not yet published")
    
    @staticmethod
    def confirm_transaction(transaction):
        # Probably confirmation this way is not totally realisitc,
        # as any user technically can hence delete a registered (broadcasted),
        # un confirmed transaction before it gets published or the real
        # recipient recieves it; with the need for it be re-registered, although
        # enough for controlled simulation
        if Ledger.__instance is None:
            logging.error("No Ledger is created")
            return None
        for t in Ledger.__instance._unconfirmed_transactions:
            if transaction == t:
                Ledger.__instance._unconfirmed_transactions.remove(transaction)
                logging.info("Ledger :: Transaction is confirmed by recipient")
                return True
        logging.error("Ledger :: No such transaction exists on the queue")
        return False
    
    @staticmethod
    def get_incoming_transactions(recipient_vk):
        if Ledger.__instance is None:
            logging.error("No Ledger is created")
            return None
        coming_transactions = []
        for t in Ledger.__instance._unconfirmed_transactions:
            if t.recipient_vk == recipient_vk:
                coming_transactions.append(t)
        return coming_transactions
    
    
    @staticmethod       
    def get_coins(user_vk, amount=-1):
        if Ledger.__instance is None:
            logging.error("No Ledger is created")
            return None
        available_coins = Ledger.__instance._users_coins[user_vk]
        if len(available_coins) < amount & amount != -1:
            return None
        to_spend_coins = available_coins[:amount]
        return to_spend_coins
    
    @staticmethod
    def add_user(user_vk):
        if Ledger.__instance is None:
            return None
        Ledger.__instance._users_coins[user_vk] = []

    @staticmethod
    def view_users():
        if Ledger.__instance is None:
            logging.error("No Ledger is created")
            return None
        return Ledger.__instance._users_coins.copy()
    
    @staticmethod
    def get_last_hash_pts():
        if Ledger.__instance is None:
            logging.error("No Ledger is created")
            return None
        return (Ledger._last_hash_pt_signed, Ledger._last_hash_pt)
    
    @staticmethod
    def verify_transaction_existance(transaction):
        if Ledger.__instance is None:
            logging.error("No Ledger is created")
            return None
        logging.info("Ledger :: Using merkle_trees to verify")
        proof = Ledger.__instance._merkle_tree.get_proof(transaction.hash)

        if Ledger.__instance._merkle_tree.verify_leaf_inclusion(transaction.hash, proof):
            logging.info("Ledger :: Transaction exists in the blockchain")
            return True
        logging.error("Ledger :: Transaction does NOT exist in the blockchain")
        return False
        
    @staticmethod
    def print_merkle_tree():
        if Ledger.__instance is None:
            logging.error("No Ledger is created")
            return None
        beautify(Ledger.__instance._merkle_tree)
        
        