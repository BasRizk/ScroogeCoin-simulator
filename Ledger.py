import random 
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
    
    def add_block(self, block):
        # Apply Block Transactions (Exchange Coins)
        for t in block.transactions:
            consumed_coins = t.coins
            sender_coins = self._users_coins[t.sender_vk]
            left_over_coins =\
                [c for c in sender_coins if c not in consumed_coins]
            self._users_coins[t.sender_vk] = left_over_coins
            random.shuffle(self._users_coins[t.sender_vk])
            self._users_coins[t.recipient_vk] = self._users_coins[t.recipient_vk] + consumed_coins
            random.shuffle(self._users_coins[t.recipient_vk])
        self._merkle_tree.extend(block.transactions)
        logging.info("A Block is published")
        
    @staticmethod       
    def get_coins(user_vk, amount=-1):
        if Ledger.__instance is None:
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
        return (Ledger._last_hash_pt_signed, Ledger._last_hash_pt)
    
    @staticmethod
    def verify_transaction_existance(transaction):
        proof = Ledger.__instance._merkle_tree.get_proof(transaction)

        if tree.verify_leaf_inclusion(transaction, proof):
            return True
        return False
        
        
        