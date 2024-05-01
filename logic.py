import logging
import os
import jwt
import sqlite3
from datetime import datetime, timedelta

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Определение пути к файлу базы данных в поддиректории 'data'
db_path = os.path.join('data', 'gv.db')