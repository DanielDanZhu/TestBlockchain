import hashlib as hasher
import datetime as date

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
    return Block(0, date.datetime.now(), "Genesis Block", "0")

def make_block(last_block):
    new_index = last_block.index + 1
    new_timestamp = date.datetime.now()
    new_data = "Block " + str(new_index)
    new_previous_hash = last_block.hash_block()
    return Block(new_index, new_timestamp, new_data, new_previous_hash)

blockchain = [make_genesis()]
previous_block = blockchain[0]

for i in range(0, 20):
  block_to_add = make_block(previous_block)
  blockchain.append(block_to_add)
  previous_block = block_to_add
  print("Block #{} has been added to the blockchain!".format(block_to_add.index))
  print("Hash: {}\n".format(block_to_add.hash))
