import logging
import os
import random
import sqlite3
import string

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Определение пути к файлу базы данных
db_path = os.path.join('app', 'tma.db')

def generate_nickname() -> str:
    logger.info("generate_nickname called")

    adjectives = ['Happy', 'Silly', 'Brave', 'Cute', 'Clever', 'Crazy', 'Fancy', 'Jolly', 'Lucky', 'Sunny']
    nouns = ['Panda', 'Kitten', 'Puppy', 'Rabbit', 'Turtle', 'Dolphin', 'Monkey', 'Giraffe', 'Koala', 'Penguin']

    while True:
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        number = ''.join(random.choices(string.digits, k=4))
        nickname = f"{adjective}{noun}{number}"

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users WHERE nickname = ?", (nickname,))
        count = c.fetchone()[0]
        conn.close()

        if count == 0:
            return nickname

def create_user_db(wallet_address: str) -> object:
    logger.info("create_user_db called")
    conn = None

    try:
        nickname = generate_nickname()
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO users (wallet_address, nickname) VALUES (?, ?)", (wallet_address, nickname))
        user_id = c.lastrowid
        conn.commit()
        return {'user_id': user_id, 'wallet_address': wallet_address, 'nickname': nickname}
    
    except sqlite3.IntegrityError:
        logger.error("User with wallet address %s already exists", wallet_address)
        return None
    
    finally:
        if conn is not None:
            conn.close()