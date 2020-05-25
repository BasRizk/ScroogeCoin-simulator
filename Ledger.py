class Ledger:

    def __init__(self, users_vk):
        self.last_hash_pt = None
        self.last_hash_pt_signed = None
        self.users_vk = users_vk

    def __str__(self):
        block = self.last_hash_pt[0]
        blockchain = ''
        while True:
            blockchain += (str(block) + '\n')
            block = block.prev_hash_pt[0]
        return blockchain