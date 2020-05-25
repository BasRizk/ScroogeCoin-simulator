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
import Scrooge, User, Ledger


def run_simulation():
    users = []
    for i in range(10):
        user = User()
        users.append(user)
    vks = [user.vk for user in users]
    blockchain = Scrooge(vks)
    for i in users:
        print(user.vk + ':\t' + str(len(user.coins)))
    blockchain.run()
    
    # TODO - MOVED FROM SCROOGE - Create the initial coins
    for vk in users_vk:
        self.create_coin_transaction(vk, 10)

    

if __name__ == '__main__':
    run_simulation()
    
    
# General Notes

#------ TODO
# 8- Scrooge will create and sign the 10 initial scrooge coins for each user.
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


# Output Format

# ❖ Print initially the public key and the amount of coins for each user.
# ❖ Scoorge should print the block under construction for each new
# transaction added (include the transaction details).
# ❖ Print the blockchain after a new block is appended.
# ❖ Terminate the code using the key ‘Space’.
# ❖ Save all the printed data to a text file upon termination

