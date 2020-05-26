# -*- coding: utf-8 -*-

class MerkleTree:
    
    def __init__(self):
        pass
    
    def generate_merkle_root(self):
        pass
    
"""
- If there happens to be an odd number of inputs,
  then the last input is copied and paired with itself
  
- Let’s say that a single block contains a total of 424 transactions.
  The Merkle Tree would start by grouping these transactions into 212 pairs.
  The next step is for the 212 transaction ID pairs to go through a hashing
  function. This would result in 212 new 64-character codes
- The 212 new codes would be paired up and turned into 106 pairs.
- The process is repeated again, cutting the number of codes in half each time,
  until only one code remains. That code is the Merkle Root.
"""