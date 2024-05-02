import sqlite3

# Установка соединения с базой данных (создание нового файла, если он не существует)
conn = sqlite3.connect('tma.db')

# Создание таблицы users с автоматическим заполнением поля created_at
conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userid INTEGER PRIMARY KEY,
        wallet_address TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        nickname TEXT
    )
''')

# Создание таблицы licenses
conn.execute('''
    CREATE TABLE IF NOT EXISTS licenses (
        licenseid INTEGER PRIMARY KEY
    )
''')

# Создание связующей таблицы user_licenses
conn.execute('''
    CREATE TABLE IF NOT EXISTS user_licenses (
        userid INTEGER,
        licenseid INTEGER,
        FOREIGN KEY (userid) REFERENCES users (userid),
        FOREIGN KEY (licenseid) REFERENCES licenses (licenseid)
    )
''')

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
conn.close()

print("База данных успешно создана!")