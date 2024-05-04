import random
import sqlite3
import string
from .config import LOGGER, DB_PATH

def generate_nickname(max_attempts:int = 100) -> str:
    LOGGER.info("generate_nickname called")

    adjective_list = ['Happy', 'Silly', 'Brave', 'Cute', 'Clever', 'Crazy', 'Fancy', 'Jolly', 'Lucky', 'Sunny']
    noun_list = ['Panda', 'Kitten', 'Puppy', 'Rabbit', 'Turtle', 'Dolphin', 'Monkey', 'Giraffe', 'Koala', 'Penguin']

    attempt_count = 0
    while attempt_count < max_attempts:
        adjective = random.choice(adjective_list)
        noun = random.choice(noun_list)
        number = ''.join(random.choices(string.digits, k=4))
        nickname = f"{adjective}{noun}{number}"

        try:
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute(f"SELECT COUNT(*) FROM users WHERE nickname = ?", (nickname,))
                count = c.fetchone()[0]

            if count == 0:
                return nickname
            
        except sqlite3.Error as e:
            LOGGER.error(f"Database error: {e}")
            raise Exception("An error occurred with the database operation") from e

        attempt_count += 1

    raise Exception("Failed to generate a unique nickname after multiple attempts")

def create_user_db(wallet_address: str) -> object:
    LOGGER.info("create_user_db called")

    try:
        nickname = generate_nickname()
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            
            # Проверка существования пользователя с таким wallet_address
            c.execute("SELECT 1 FROM users WHERE wallet_address = ?", (wallet_address,))
            if c.fetchone():
                raise ValueError("User with this wallet address already exists")
            
            c.execute("INSERT INTO users (wallet_address, nickname) VALUES (?, ?)", (wallet_address, nickname))
            user_id = c.lastrowid
            conn.commit()

            return {'user_id': user_id, 'wallet_address': wallet_address, 'nickname': nickname}
    
    except sqlite3.IntegrityError as e:
        LOGGER.error(f"Integrity error: {e}")
        raise ValueError("User with this wallet address already exists") from e
    
    except sqlite3.Error as e:
        LOGGER.error(f"Database error: {e}")
        raise Exception("An error occurred with the database operation") from e
    
def get_user_by_params(user_id: str = None, wallet_address: str = None, nickname: str = None) -> object:
    LOGGER.info("get_user_by_params_db called")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            
            query = f"SELECT * FROM users WHERE "
            params = []

            if user_id:
                query += "userid = ?"
                params.append(user_id)
            elif wallet_address:
                query += "wallet_address = ?"
                params.append(wallet_address)
            elif nickname:
                query += "nickname = ?"
                params.append(nickname)
            else:
                raise ValueError("Invalid parameter provided")

            c.execute(query, params)
            row = c.fetchone()

            if row:
                return {
                    'user_id': row[0],
                    'wallet_address': row[1],
                    'created_at': row[2],
                    'nickname': row[3]
                }
            else:
                return None
    
    except sqlite3.Error as e:
        LOGGER.error(f"Database error: {e}")
        raise Exception("An error occurred with the database operation") from e