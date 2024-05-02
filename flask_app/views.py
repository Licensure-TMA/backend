import logging
from flask import jsonify, request
from .auth import token_required
from . import app
from . import logic
from . import limiter

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
    
@app.route('/api/test', methods=['GET'])
@limiter.limit("10 per minute")
@token_required
def test():
    return jsonify({'test': "ok!"}), 200

@app.route('/api/createUser', methods=['POST'])
@limiter.limit("10 per minute")
@token_required
def create_user():
    data = request.get_json()
    wallet_address = data.get('wallet_address')

    if not wallet_address:
        return jsonify({'error': 'Wallet address are required'}), 400

    try:
        result = logic.create_user_db(wallet_address)
        return jsonify(result), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500