import jwt
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.environ.get('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Извлекаю токен из заголовка Authorization
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")
        
        # Если токен отсутствует, верну ошибку
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Декодирование токена
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 403
        except Exception:
            return jsonify({'message': 'An error occurred while validating the token'}), 500

        # Передаю управление декорированной функции
        return f(*args, **kwargs)

    return decorated