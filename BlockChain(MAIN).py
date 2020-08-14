import hashlib
import json
from time import time 

"""Responsible for managing chain """


class Blockchain(object):
    def __init__(self):
        self.chain= []
        self.current_transactions = []

        # Create genesis block
        self.new_block(previous_hash=1,proof = 1000)
    
    def new_block(self,proof,previous_hash=None):
        # Create new block and add it into chain
        block = {
            'index': len(self.chain) +1,
            'timestamp': time(),
            'transcation': self.current_transactions,
            'proof': proof,
            'previous_hash': self.previous_hash or self.hash(self.chain[-1]),  

        }

        # Reset the current list of transcation
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self,sender,recipient,amount):
        """
        Create a new transcation to go into next mined block


        """

        self.current_transactions.append({
            'sender':sender,
            'recipient': recipient,
            'amount':amount,
        })

        return self.last_block['index'] + 1





    @staticmethod
    def hash(block):
        # Hashes Block
        """
        Create a SHA-256 hash of a block
        :param block : <dict> Block
        :return <str>
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string= json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    @property 
    def last_block(self):
        # Return the last blck of the chain
        return self.chain[-1]




    

