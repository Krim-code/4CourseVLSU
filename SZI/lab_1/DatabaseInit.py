import sqlite3


class DatabaseInitializer:
    def __init__(self, db_name):
        self.db_name = db_name

    def initialize_database(self):
        # Подключение к базе данных
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Создание таблицы "users", если она не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                is_blocked BOOLEAN DEFAULT 0
            )
        ''')
        conn.commit()

        # Проверка, существует ли пользователь ADMIN
        cursor.execute('SELECT id FROM users WHERE username = ?', ('ADMIN',))
        admin_id = cursor.fetchone()

        if not admin_id:
            # Добавление пользователя ADMIN с паролем "1234Br.1"
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('ADMIN', '1234Br.1!'))
            conn.commit()

        # Закрытие соединения с базой данных
        conn.close()
