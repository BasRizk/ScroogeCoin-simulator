"""
In this project, we will design a cryptocurrency similar to ScroogeCoin. 

- A network of 100 users will simulate the transaction processes.

- Initially each user will have 10 ScroogCoins.

- As long as the system is running, a random transaction with random amount
  (within the range of amount the user has) will be created from User A to
  User B.

- The transaction is signed by the private-key of the sender.

- Scrooge get notified by every transaction.
- Scrooge verifies the signature before accumulating the transaction.

- Once Scrooge accumulates 10 transaction, he can form a block and attach it to 
  the blockchain.

- You are allowed to use predefined hash and digital signature libraries.
  Mention which libraries you used.
"""
from Scrooge import Scrooge
from User import User
from Ledger import Ledger

import keyboard
import random 
import logging
"""
=>> Output Format

❖ Print initially the public key and the amount of coins for each user.
❖ Scoorge should print the block under construction for each new
   transaction added (include the transaction details).
❖ Print the blockchain after a new block is appended.
❖ Terminate the code using the key ‘Space’.
❖ Save all the printed data to a text file upon termination

"""
class Simulator:
    
    def __init__(self):
        self.init_logger() 
        
        self.scrooge = Scrooge()
        self.users = []
        for i in range(10):
            user = User()
            self.users.append(user)
        
        # self.vks = [user.vk for user in self.users]
    
    def init_logger(self):
        # logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")    
        logging.basicConfig(
            level=logging.INFO,
            format="%(msecs)d : [%(levelname)-5.5s] %(message)s",
            handlers=[
                logging.FileHandler("debug.log", mode='w'),
                logging.StreamHandler()
            ]
        )
        
        logging.getLogger().setLevel(logging.DEBUG)
        
    def get_current_users(self):
        users = list(Ledger.view_users().keys())
        users.remove(self.scrooge.vk)
        return users
    
    def run_simulation(self, DEBUG_MODE):
        
        logging.info('Start - Empty Wallets')
        logging.info('----------------------------------')
        users_coins_dict = Ledger.view_users()
        for user in self.users:
            logging.info(user.vk + ':\t' + str(len(users_coins_dict[user.vk])))
            logging.info('----------------------------------')
        logging.info('----------------------------------')
        
        
        logging.info('The initial 10 coin transactions')
        logging.info('----------------------------------')
        # Initially each user will have 10 ScroogCoins
        for vk in self.get_current_users():
            self.scrooge.create_coin_transaction(vk, 10)
        logging.info('----------------------------------')
        
        # logging.info('Users to confirm incoming transactions')
        # for i, recipient in enumerate(self.users):
        #     incoming_transactions =\
        #                 recipient.get_incoming_transactions()
        #     logging.debug("incoming_transactions of user %d are %d" % (i, len(incoming_transactions)))
        #     while(len(incoming_transactions) > 0):
        #         recipient.confirm_incoming_transaction(
        #                 incoming_transactions.pop(),
        #                 verify=True
        #                 )                
        # logging.info('----------------------------------')

        
        
        logging.info('Inital amount of coins per user')
        logging.info('----------------------------------')
        users_coins_dict = Ledger.view_users()
        for user in self.users:
            logging.info(user.vk + ':\n' + str(len(users_coins_dict[user.vk])))
        logging.info('----------------------------------')
        
        
        logging.info('START SIMULATION')
        logging.info('----------------------------------')
        while(True):
            debug_attack = False
            verification_attack = False
            print_merkle_tree =  False
            if DEBUG_MODE:
                logging.debug("DEBUG MODE: Press Enter for next step." +
                              " Press 'D' for Double Spending Attack. Press" +
                              " 'O' to generate a transaction on behalf of " +
                              "someone else. Press 'M' to print merkle Tree" +
                              " in CONSOLE\n\n")
    
            while DEBUG_MODE:
                if keyboard.is_pressed('\n'):
                    break
                if keyboard.is_pressed(' '):
                    logging.debug('Space is pressed')
                    return
                if keyboard.is_pressed('d'):
                    logging.debug('Double Spending Attack')
                    debug_attack = True
                    break
                if keyboard.is_pressed('o'):
                    logging.debug('Attack Verification')
                    verification_attack = True
                    break
                if keyboard.is_pressed('m'):
                    logging.debug('Merke Tree in console')
                    print_merkle_tree = True
                    break
            else:
                if keyboard.is_pressed(' '):
                    logging.debug('Space is pressed')
                    return
            
            if print_merkle_tree:
                Ledger.print_merkle_tree()
                continue
            
            sender = random.choice(self.users)
            sender_vk = sender.vk
            while True:
                recipient = random.choice(self.users)
                # recipient_vk = random.choice(self.vks)
                recipient_vk = recipient.vk
                if sender_vk != recipient_vk:
                    break
                
            if len(Ledger.view_users()[sender_vk]) >= 1:
                wallet = Ledger.view_users()[sender_vk]
                amount = random.randint(1, len(wallet))
                double_spending_attack_chance = debug_attack if DEBUG_MODE else random.choices([True, False],[1,20],1) # [1,1] are wights for the choices
                transaction = sender.pay(amount, recipient_vk)
                if verification_attack:
                    logging.info("WARNING :: A verification attack to happen..")
                    while True:
                        hack_sender = random.choice(self.get_current_users())
                        if hack_sender != transaction.sender_vk:
                            break
                    transaction.sender_vk = hack_sender
    
                if transaction:
                    # handle = self.scrooge.handle_payment_transaction(transaction)
                    self.scrooge.handle_next_transaction()
                    incoming_transactions = recipient.get_incoming_transactions()
                    if incoming_transactions is not None and \
                        len(incoming_transactions) > 0:
                        recipient.confirm_incoming_transaction(incoming_transactions.pop(),
                                                               verify= True)
                    else:
                        logging.info("A transaction seems to been dropped.")
            
                    
                    # if not handle and DEBUG_MODE:
                    #     for user in users:
                    #         logging.debug(user.vk + ':\n' + str(len(Ledger.view_users()[user.vk])))
                    if double_spending_attack_chance:
                        logging.info("WARNING :: A double spending attack to happen..")
                        recipient = random.choice(self.users)
                        # recipient_vk = random.choice(self.vks)
                        recipient_vk = recipient.vk
                        # transaction_double = 
                        sender.pay(amount, recipient_vk, transaction.coins)
                        # handle = self.scrooge.handle_payment_transaction(transaction_double)
                        
                        # TODO ask simulator if wanna simulate falling under_double spending attack
                        user_may_fall_under_double_spending_attack = False
                        # User confirms without verification before scrooge actually publish
    
                        incoming_transactions =\
                            recipient.get_incoming_transactions()
                        recipient.confirm_incoming_transaction(
                            incoming_transactions.pop(),
                            verify= not user_may_fall_under_double_spending_attack
                            )
                        
                        self.scrooge.handle_next_transaction()
                        if not user_may_fall_under_double_spending_attack:
                            incoming_transactions =\
                                recipient.get_incoming_transactions()
                            recipient.confirm_incoming_transaction(
                                incoming_transactions.pop(),
                                verify= not user_may_fall_under_double_spending_attack
                                )
                        # TODO maybe verify manually here using the Ledger if transaction got published
                        #  and if not and user_may_fall_under_double_spending_attack, then anounce the error
                        #  in simulation
                        
                        
                        
                        
                        # if not handle and DEBUG_MODE:
                        #     for user in users:
                        #         logging.debug(user.vk + ':\n' + str(len(Ledger.view_users()[user.vk])))
                debug_attack = False
                verification_attack = False
                
        # Release file
        logging.shutdown()


if __name__ == '__main__':
    simulator = Simulator()
    simulator.run_simulation(DEBUG_MODE=True)
    del simulator
    
# General Notes

#------ TODO
# 9- A user cannot confirm a transaction unless it is published on the blockchain.
# 10- Additional transaction verification should be applied using the Merkel Tree.

#------ DONE
# 1- Each coin should have a coin ID. 
# 2- Each transaction should have a transaction ID, a hash pointer to the
# previous. transaction, the amount of coins and signed by the sender.
# 3- Each block in the blockchain should have a block ID, 10 valid
# transactions, a hash of the block, and a hash pointer to the previous block.
# 4- The final hash pointer should be signed by Scrooge.
# 5- Scrooge verifies that the transaction belongs to the owner.
# 6- Scrooge verifies that the transaction is not a Double spending.
# 7- If 5 and 6 are verified Scrooge publishes the transaction to the block.





#  Deliverables


#  ---- Some distributed over files

# ❖ A simulation of the network, with multiple users and the randomized
# process of making a transaction, making each transaction reach an arbitrary user.


# ❖ For digital signature, use any of the technique described throughout the course.

# ❖ Implement Merkel Tree for the blockchain you create. The Merkel Tree
# should reflect the change in the blockchain when adding a new block to
# the blockchain.
# ❖ Transaction verification using Merkel Tree to make sure that the coins
# are not spent before by the same user.

