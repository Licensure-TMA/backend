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
    return jsonify({'test': "ok"}), 200