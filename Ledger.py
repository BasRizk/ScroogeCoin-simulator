class Ledger:

    def __init__(self, users_vk):
        self.last_hash_pt = None
        self.last_hash_pt_signed = None
        self.users_vk = users_vk