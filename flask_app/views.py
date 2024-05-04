from .config import LOGGER
from flask import jsonify, request
from .auth import token_required
from . import app
from . import logic
from . import limiter
    
@app.route('/api/test', methods=['GET'])
@limiter.limit("10 per minute")
@token_required
def test():
    LOGGER.info('test called')

    return jsonify({'message': "OK"}), 200

@app.route('/api/createUser', methods=['POST'])
@limiter.limit("4 per minute")
@token_required
def create_user():
    LOGGER.info('create_user called')

    data = request.get_json()
    wallet_address = data.get('wallet_address')

    if not wallet_address:
        return jsonify({'error': 'Wallet address are required'}), 400

    try:
        result = logic.create_user_db(wallet_address)
        return jsonify(result), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/getUser', methods=['GET'])
@limiter.limit("4 per minute")
@token_required
def get_user():
    LOGGER.info('get_user called')

    user_id = request.args.get('user_id')
    wallet_address = request.args.get('wallet_address')
    nickname = request.args.get('nickname')

    if sum(bool(param) for param in [user_id, wallet_address, nickname]) != 1:
        return jsonify({'error': 'Exactly one parameter (user_id, wallet_address, or nickname) is required'}), 400

    try:
        user = logic.get_user_by_params(user_id, wallet_address, nickname)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500