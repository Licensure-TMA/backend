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
    
def add_license_to_user(license_id: str, user_id: str = None, wallet_address: str = None, nickname: str = None) -> str:
    LOGGER.info("add_license_to_user_db called")

    if not (user_id or wallet_address or nickname):
        LOGGER.error("No valid user parameter provided")
        raise ValueError("No valid user parameter provided")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()

            # Определение используемого параметра пользователя
            if user_id:
                param = user_id
                column = "userid"
            elif wallet_address:
                param = wallet_address
                column = "wallet_address"
            elif nickname:
                param = nickname
                column = "nickname"

            # Получение user_id по заданному параметру
            c.execute(f"SELECT userid FROM users WHERE {column} = ?", (param,))
            row = c.fetchone()
            if not row:
                LOGGER.info("No user found with the given parameters")
                return "user_not_found"
            user_id = row[0]

            # Проверка наличия лицензии с таким же license_id
            c.execute("SELECT COUNT(*) FROM licenses WHERE licenseid = ?", (license_id,))
            count = c.fetchone()[0]
            if count > 0:
                LOGGER.info(f"License {license_id} already exists")
                return "license_already_exists"

            # Добавление лицензии в таблицу licenses
            c.execute("INSERT INTO licenses (licenseid) VALUES (?)", (license_id,))

            # Связывание лицензии с пользователем в таблице user_licenses
            c.execute("INSERT INTO user_licenses (userid, licenseid) VALUES (?, ?)", (user_id, license_id))

            conn.commit()
            LOGGER.info(f"License {license_id} added and linked to user {user_id}")
            return "success"

    except sqlite3.Error as e:
        LOGGER.error(f"Database error: {e}")
        conn.rollback()
        raise Exception("An error occurred with the database operation") from e
    
def get_user_by_license_id(license_id: str) -> dict:
    LOGGER.info("get_user_by_license_id_db called")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT u.userid, u.wallet_address, u.created_at, u.nickname, l.licenseid
                FROM users u
                JOIN user_licenses ul ON u.userid = ul.userid
                JOIN licenses l ON ul.licenseid = l.licenseid
                WHERE l.licenseid = ?
            """, (license_id,))
            row = c.fetchone()

            if row:
                user_data = {
                    'user_id': row[0],
                    'wallet_address': row[1],
                    'created_at': row[2],
                    'nickname': row[3]
                }
                LOGGER.info(f"User found for license {license_id}")
                return user_data
            else:
                LOGGER.info(f"No user found for license {license_id}")
                return None
            
    except sqlite3.Error as e:
        LOGGER.error(f"Database error: {e}")
        raise Exception("An error occurred with the database operation") from e
    
def get_licenses_by_user_params(user_id: str = None, wallet_address: str = None, nickname: str = None) -> list:
    LOGGER.info("get_licenses_by_user_params_db called")

    if not (user_id or wallet_address or nickname):
        LOGGER.error("No valid user parameter provided")
        raise ValueError("No valid user parameter provided")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()

            if user_id:
                param = user_id
                column = "userid"
            elif wallet_address:
                param = wallet_address
                column = "wallet_address"
            elif nickname:
                param = nickname
                column = "nickname"

            c.execute(f"""
                SELECT l.licenseid
                FROM licenses l
                JOIN user_licenses ul ON l.licenseid = ul.licenseid
                JOIN users u ON ul.userid = u.userid
                WHERE u.{column} = ?
            """, (param,))
            rows = c.fetchall()

            if rows:
                licenses_data = [{'license_id': row[0]} for row in rows]
                LOGGER.info(f"Licenses found for user with {column} = {param}")
                return licenses_data
            else:
                LOGGER.info(f"No licenses found for user with {column} = {param}")
                return None

    except sqlite3.Error as e:
        LOGGER.error(f"Database error: {e}")
        raise Exception("An error occurred with the database operation") from e
    
def delete_license_by_id(license_id: str) -> bool:
    LOGGER.info("delete_license_by_id_db called")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()

            # Удаление связи из таблицы user_licenses
            c.execute("DELETE FROM user_licenses WHERE licenseid = ?", (license_id,))

            # Удаление лицензии из таблицы licenses
            c.execute("DELETE FROM licenses WHERE licenseid = ?", (license_id,))
            licenses_deleted = c.rowcount

            conn.commit()

            if licenses_deleted > 0:
                LOGGER.info(f"License {license_id} and associated user licenses deleted")
                return True
            else:
                LOGGER.info(f"License {license_id} not found")
                return False

    except sqlite3.Error as e:
        LOGGER.error(f"Database error: {e}")
        conn.rollback()
        raise Exception("An error occurred with the database operation") from e