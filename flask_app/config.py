import logging
import os

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Определение пути к файлу базы данных
DB_PATH = os.path.join('tma.db')