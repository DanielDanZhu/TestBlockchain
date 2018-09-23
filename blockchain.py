from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date
node = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

def make_genesis():
    return Block(0, date.datetime.now(), {"proof-of-work": 9, "transactions": None}, 0)

def make_block(last_block):
    new_index = last_block.index + 1
    new_timestamp = date.datetime.now()
    new_data = "Block " + str(new_index)
    new_previous_hash = last_block.hash_block()
    return Block(new_index, new_timestamp, new_data, new_previous_hash)

blockchain = [make_genesis()]
previous_block = blockchain[0]

miner_address = "Amazing Grace"
miners_reward = 2

this_nodes_transactions = []
peer_nodes = []

@node.route('/txion', methods=['POST'])
def transaction():
    new_txion = request.get_json()
    this_nodes_transactions.append(new_txion)
    print("New transaction")
    print("FROM: {}".format(new_txion['from']))
    print("TO: {}".format(new_txion['to']))
    print("AMOUNT: {}\n".format(new_txion['amount']))
    return "Transaction successful"

def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 5 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor

@node.route('/mine', methods = ['GET'])
def mine():
    last_block = blockchain[-1]
    last_proof = last_block.data['proof-of-work']
    proof = proof_of_work(last_proof)
    this_node_transactions.append(
        {"from": "network", "to": miner_address, "amount": miners_reward}
    )
    new_block_data = {
        "proof-of-work": proof,
        "transactions": this_nodes_transactions
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = date.datetime.now()

    this_nodes_transactions = []
    new_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block.hash
    )
    blockchain.append(new_block)
    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block.hash
    }) + "\n"

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain
    for block in chain_to_send:
        block = {
            "index": str(block.index),
            "timestamp": str(block.timestamp),
            "data": str(block.data),
            "hash": block.hash
        }
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send

def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        block = requests.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains

def consensus():
    other_chains = find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    blockchain = longest_chain

@node.run
