import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request, send_from_directory

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, product_id, product_name, status):
        
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'product_id': product_id,
            'product_name': product_name,
            'status': status,
        })

        return self.last_block['index'] + 1

    def get_product_history(self, product_id):

        product_history = []
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['product_id'] == product_id:
                    product_history.append(transaction)
        return product_history

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
       
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        product_id="",
        product_name="Mining Reward",
        status="mined",
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Found",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'product_id', 'product_name', 'status']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['product_id'], values['product_name'], values['status'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/product/<string:product_id>', methods=['GET'])
def get_product(product_id):
    product_history = blockchain.get_product_history(product_id)
    if product_history:
        response = {
            'product_id': product_id,
            'history': product_history,
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': 'Product not found'}), 404


@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('', path)

@app.route('/verify-authenticity/<product_id>', methods=['GET'])
def verify_authenticity(product_id):
    product_history = blockchain.get_product_history(product_id)
    if product_history:
        is_authentic = True  # Additional logic to verify authenticity
        return jsonify({
            'is_authentic': is_authentic,
            'history': product_history
        }), 200
    else:
        return jsonify({'message': 'Product not found or not authentic'}), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
