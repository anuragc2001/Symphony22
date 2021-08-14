import datetime
import hashlib
import json
from pathlib import Path
from apis import update_blockchain, get_blockchain


def update_local_storage(blockchain):
    data = json.dumps(blockchain, indent=4)
    Path("local_chain.json").write_text(data)


class Blockchain:

    def __init__(self):
        blockchain = get_blockchain()
        if "chain" not in blockchain or len(blockchain["chain"]) == 0:
            self.chain = []
            gen_block = self.create_block(nonce=1, previous_hash='0', data="Big bang", current_hash=None)
            hashed_gen_block = self.hash(gen_block)
            nonce, current_hash = self.proof_of_work(hashed_gen_block)
            gen_block['nonce'] = nonce
            gen_block['current_hash'] = current_hash
            self.add_block_to_blockchain(gen_block)
        else:
            self.chain = blockchain["chain"]

    def sync_with_server(self):
        blockchain = get_blockchain()
        if "chain" not in blockchain:
            self.chain = []
        elif len(blockchain["chain"]) != len(self.chain):
            self.chain = blockchain["chain"]

    def update_server(self):
        blockchain = get_blockchain()
        blockchain_dict = {
            "chain": []
        }
        blockchain_dict["chain"] = self.chain
        update_blockchain(blockchain_dict)
        update_local_storage(blockchain)

    def create_block(self, nonce, previous_hash, current_hash, data):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now(datetime.timezone.utc)),
            'data': data,
            'nonce': nonce,
            'previous_hash': previous_hash,
            'current_hash': current_hash
        }
        return block

    def add_block_to_blockchain(self, block):
        self.chain.append(block)
        self.update_server()

    def print_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, hashed_block):
        nonce = 0
        check_nonce = False
        current_hash = None
        while check_nonce is False:
            hash = hashlib.sha256(str(str(nonce) + str(hashed_block)).encode()).hexdigest()
            if hash[:4] == '0000':
                current_hash = hash
                check_nonce = True
            else:
                nonce += 1
        return nonce, current_hash

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        self.sync_with_server()
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            data = block['data']
            block_copy = {
                'index': block['index'],
                'timestamp': block['timestamp'],
                'data': data,
                'nonce': 0,
                'previous_hash': previous_block['current_hash'],
                'current_hash': None
            }
            block_hash_copy = self.hash(block_copy)
            c_nonce, current_hash = self.proof_of_work(block_hash_copy)

            if current_hash != block['current_hash'] and c_nonce != block['nonce']:
                return False

            if current_hash[:4] != '0000':
                return False
            previous_block = block
            block_index += 1

        return True
