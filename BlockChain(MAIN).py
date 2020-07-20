"""Responsible for managing chain """


class Blockchain(object):
    def __init__(self):
        self.chain= []
        self.current_transactions = []
    
    def new_block(self):
        # Create new block and add it into chain 
        pass

    def transaction(self):
        # add transcation to the list of current transcation
        pass

    @staticmethod
    def hash(block):
        # Hashes Block
        pass


    @property 
    def last_block(self):
        # Return the last blck of the chain
        pass


