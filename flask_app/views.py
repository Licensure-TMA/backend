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
    
@app.route('/api/addLicense', methods=['POST'])
@limiter.limit("4 per minute")
@token_required
def add_license():
    LOGGER.info('add_license called')

    data = request.get_json()
    license_id = data.get('license_id')
    user_id = data.get('user_id')
    wallet_address = data.get('wallet_address')
    nickname = data.get('nickname')

    if not license_id:
        return jsonify({'error': 'license_id is required'}), 400

    if sum(bool(param) for param in [user_id, wallet_address, nickname]) != 1:
        return jsonify({'error': 'Exactly one user parameter (user_id, wallet_address, or nickname) is required'}), 400

    try:
        result = logic.add_license_to_user(license_id, user_id, wallet_address, nickname)
        if result == "success":
            return jsonify({'message': 'License added successfully'}), 201
        elif result == "user_not_found":
            return jsonify({'error': 'User not found'}), 404
        elif result == "license_already_exists":
            return jsonify({'error': 'License already exists'}), 409
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/getUserByLicense', methods=['GET'])
@limiter.limit("10 per minute")
@token_required
def get_user_by_license():
    LOGGER.info('get_user_by_license called')

    license_id = request.args.get('license_id')

    if not license_id:
        return jsonify({'error': 'license_id is required'}), 400

    try:
        user_data = logic.get_user_by_license_id(license_id)
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({'error': 'User not found for the given license'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/getLicensesByUser', methods=['GET'])
@limiter.limit("10 per minute")
@token_required
def get_licenses_by_user():
    LOGGER.info('get_licenses_by_user called')

    user_id = request.args.get('user_id')
    wallet_address = request.args.get('wallet_address')
    nickname = request.args.get('nickname')

    if sum(bool(param) for param in [user_id, wallet_address, nickname]) != 1:
        return jsonify({'error': 'Exactly one user parameter (user_id, wallet_address, or nickname) is required'}), 400

    try:
        licenses_data = logic.get_licenses_by_user_params(user_id, wallet_address, nickname)
        if licenses_data:
            return jsonify(licenses_data), 200
        else:
            return jsonify({'error': 'No licenses found for the given user'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/deleteLicense', methods=['DELETE'])
@limiter.limit("4 per minute")
@token_required
def delete_license():
    LOGGER.info('delete_license called')

    license_id = request.args.get('license_id')

    if not license_id:
        return jsonify({'error': 'license_id is required'}), 400

    try:
        success = logic.delete_license_by_id(license_id)
        if success:
            return jsonify({'message': 'License deleted successfully'}), 200
        else:
            return jsonify({'error': 'License not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500