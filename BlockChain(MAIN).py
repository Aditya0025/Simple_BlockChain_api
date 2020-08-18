import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse


class Blockchain(object):
    """Responsible for managing chain"""
    def __init__(self):
        self.chain= []
        self.current_transactions = []
        # we want to be sure that node are unique
        self.nodes = set()

        # creating a gensis(a coming to being) block
        self.new_block(previous_hash=1,proof=100)

    def new_block(self,proof,previous_hash):
        # Create new block and add it into chain
        # param: int(proof) the proof given by the proof of work algorithm
        # previous hash(optional)<str> has pf previous hash
        # return : <dixt> New Block 
        
        block= {
            'index': len(self.chain) +1,
            'timestamp': time(),
            'transcation': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) #calling hash function

        }

        # reset the current list of transcations
        self.current_transactions =[]
        self.chain.append(block)

        return block


    def new_transcation(self,sender, recipient,amount):
        """
        create a new transcation to go into the next mined block
        :param sender: <str> Address of the sender
        :param recipient : <str> Address of the Recipient
        :param amount : <int> Amount 
        :return <int> the index of he Block that will hold this transcation
        """
        trans = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }


        self.current_transactions.append(trans)
        print(trans)
        return self.last_block['index'] +1

    # def transaction(self):
    #     # add transcation to the list of current transcation
    #     pass

    @staticmethod
    # """Static method bound to class onlyrather than the object for that class"""

    def hash(block):
        # Hashes Block
        """
        Create a SHA-256  hash of the block
        :parm block:<dict> 
        :return : <str> 
        """
        # Dictionary must be Ordered, or we will have inconistent hashes
        block_string= json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property 
    # """ a special fucntionality to certain methods to make them act as getters,
    # setters or deleters"""
    def last_block(self):
        # Return the last blck of the chain
        return self.chain[-1]



    def proof_of_work(self,last_proof):
        """
        Simple proof of work algorithm
        -find a number p such that hash(pp') contain leading 4 zeros
        where p is the previous p' 
        - p is the previous proof and p' is the new proof
        :param last_proof : <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof +=1
        
        return proof

    
    @staticmethod
    def valid_proof(last_proof,proof):
        """  
        Validates he prppf: Does hash(lst_proof,proof) contain 4 leading zeros?
        : Param last_proof: <int> Previous Proof
        : param proof: <int> Current Proof
        : return <bool> True if the correct, Flase is not
        """

        guess = f'{last_proof}{proof}'.encode()

        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    def register_node(self,address):
        """
        Add a new node to the list of nodes
        :param address: <str> Adress of node. eg. 'http://192.168.0.5:5000'
        :return None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self,chain):
        """
        Determine if a given blockchain is valid
        : param chain: <list> A blockchain
        :return:  <bool> True if valid, Flase if not
        """

        last_block = chain[0]
        current_index= 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n ------------------- \n")
            # Check that he hash of the block is correct

            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check proof of work is correct

            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index +=1

        return True


    def resolve_conflicts(self):
        """
        This is consensus Algorithm,it resolves conflicts by replacing
        our chain with the longest one in the network. 
        :return : <bool> True if our chain was replaced,Flase if not
        """

        neighbours = self.nodes
        new_chain =None

        # we are only looking for the chains longer than ours 
        max_length  = len(self.chain)

        # Grab and verify he chains from all the nodes in our network
        for node in neighbours:
            respose = request.get(f'http://{node}/chain')
            if response.status_code==200:
                length = respose.json()['length']
                chain = respose.json()['chain']

                # Check if the length is longer and he chian is valid
                if length > max_length and self.valid_chain(chain):
                    max_length= length
                    new_chain= chain

        # Replace our chain if we dicovered a new, valid chain longer than ours

        if new_chain:
            self.chain= new_chain
            return True

        return False


    


