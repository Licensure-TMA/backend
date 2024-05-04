from functools import wraps
from flask import request, jsonify
import os

# Получаем SECRET_KEY из переменной окружения
SECRET_KEY = os.environ.get('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Извлекаем токен из заголовка Authorization
        token = request.headers.get('Authorization')

        # Если заголовок Authorization отсутствует или не содержит префикс "Bearer ", вернем ошибку
        if not token or not token.startswith("Bearer "):
            return jsonify({'error': 'Token is missing or invalid!'}), 403

        # Удаляем префикс "Bearer " и проверяем, совпадает ли токен с SECRET_KEY
        token = token[7:]  # Удалить "Bearer " из строки

        if token != SECRET_KEY:
            return jsonify({'error': 'Token is invalid'}), 403

        # Если токен валиден, передаем управление декорированной функции
        return f(*args, **kwargs)

    return decorated