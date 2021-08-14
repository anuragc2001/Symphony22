from flask import Flask, jsonify, request
from flask.json.tag import JSONTag
from Blockchain import Blockchain
from apis import get_api_keys, push_log

app = Flask(__name__)

blockchain = Blockchain()


def get_and_check():
    api_key = request.headers.get('x-api-key')
    keys = get_api_keys()

    if keys:
        for key in keys['keys']:
            if key['key'] == api_key:
                logger = "IP:" + request.remote_addr + " |USERNAME:" + key['username'] + " |PATH:" + request.full_path
                push_log(logger)
                return True

    return {
        'message': 'API Key not found or doesn\'t exist! Request the developers for a access key.',
        'version': 'Symphony22'
    }


@app.route('/')
def index():
    response = {
        'message': "Welcome to Symphony256 API System.",
        'important points':
            [
                'Request the developers for an access key to mine/view the blockchain.',
                'Do not put any private/sensitive data when mining block.'
                'Don\'t overload the server by sending too many requests at a time.',
                '''If you have any suggestions for us, kindly mailto mailatcnc@gmail.com''',
            ],
        'github_repo': 'https://github.com/anuragc2001/Symphony22',
        'API docs': 'https://documenter.getpostman.com/view/15506921/Tzz7QJXp',
        'version': 'Symphony22 v3.14'
    }
    return jsonify(response), 200


@app.route('/mine_block', methods=['POST'])
def mine_block():
    flag = get_and_check()
    if flag != True:
        return jsonify(flag), 400
    try:
        request_data = request.json
        data = request_data['data']
    except:
        response = {
            'message': "Please provide data to mine a block",
            'version': 'Symphony22 v3.14'
        }
        return jsonify(response), 400
    try:
        blockchain.sync_with_server()
        previous_block = blockchain.print_previous_block()
        block = blockchain.create_block(0, previous_block["current_hash"], None, data)
        hashed_block = blockchain.hash(block)
        nonce, current_hash = blockchain.proof_of_work(hashed_block)
        block['nonce'] = nonce
        block['current_hash'] = current_hash
        blockchain.add_block_to_blockchain(block)
        response = {
            'message': 'You just mined a block. :)',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'data': block['data'],
            'nonce': block['nonce'],
            'current_hash': current_hash,
            'previous_hash': block['previous_hash'],
            'version': 'Symphony22 v3.14'
        }
        return jsonify(response), 200
    except Exception as e:
        print(e)
        response = {
            'message': 'Sorry! Something bad must have happened. :|',
            'version': 'Symphony22 v3.14'
        }
        return jsonify(response), 500


@app.route('/get_chain', methods=['GET'])
def display_chain():
    flag = get_and_check()
    if flag != True:
        return jsonify(flag), 400
    try:
        blockchain.sync_with_server()
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain),
                    'version': 'Symphony22 v3.14'
                    }
        return jsonify(response), 200
    except Exception as e:
        response = {
            'message': 'Sorry! Something bad must have happened. :|',
            'version': 'Symphony22 v3.14'
        }
        return jsonify(response), 500


@app.route('/is_valid', methods=['PUT'])
def valid():
    flag = get_and_check()
    if flag != True:
        return jsonify(flag), 400
    try:
        blockchain.sync_with_server()
        valid = blockchain.chain_valid(blockchain.chain)
        if valid:
            response = {'message': 'The Blockchain is valid. :)'}
        else:
            response = {'message': 'The Blockchain is not valid. :('}
        return jsonify(response), 200
    except Exception as e:
        response = {
            'message': 'Sorry! Something bad must have happened. :|',
            'version': 'Symphony22 v3.14'
        }
        return jsonify(response), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug=True)
