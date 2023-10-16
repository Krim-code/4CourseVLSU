import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


class AdminWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Администратор")
        self.geometry("600x400")

        self.menu_bar = tk.Menu(self)

        # Создаем подменю "Справка"
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.about_program)
        self.menu_bar.add_cascade(label="Справка", menu=help_menu)

        self.config(menu=self.menu_bar)

        self.label = tk.Label(self, text="Добро пожаловать, администратор!")
        self.label.pack()

        self.block_user_button = tk.Button(self, text="Заблокировать пользователя", command=self.block_user)
        self.change_password_button = tk.Button(self, text="Изменить пароль пользователя", command=self.change_password)
        self.change_username_button = tk.Button(self, text="Изменить логин пользователя", command=self.change_username)
        self.add_user_button = tk.Button(self, text="Добавить пользователя", command=self.add_user)
        self.view_users_button = tk.Button(self, text="Просмотреть пользователей", command=self.view_users)
        self.delete_user_button = tk.Button(self, text="Удалить пользователя", command=self.delete_user)
        self.unblock_user_button = tk.Button(self, text="Разблокировать пользователя", command=self.unblock_user)

        self.block_user_button.pack()
        self.change_password_button.pack()
        self.change_username_button.pack()
        self.add_user_button.pack()
        self.view_users_button.pack()
        self.delete_user_button.pack()
        self.unblock_user_button.pack()

    def block_user(self):
        username = tk.simpledialog.askstring("Заблокировать пользователя", "Введите имя пользователя:")
        if not username:
            return

        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_blocked = 1 WHERE username = ?', (username,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Пользователь заблокирован", f"Пользователь {username} заблокирован.")

    def change_password(self):
        username = tk.simpledialog.askstring("Изменить пароль пользователя", "Введите имя пользователя:")
        if not username:
            return

        new_password = tk.simpledialog.askstring("Изменить пароль пользователя", "Введите новый пароль:")
        if not new_password:
            return

        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
        conn.commit()
        conn.close()
        messagebox.showinfo("Пароль изменен", f"Пароль пользователя {username} изменен.")

    def change_username(self):
        old_username = tk.simpledialog.askstring("Изменить логин пользователя", "Введите текущий логин пользователя:")
        if not old_username:
            return

        new_username = tk.simpledialog.askstring("Изменить логин пользователя", "Введите новый логин:")
        if not new_username:
            return

        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, old_username))
        conn.commit()
        conn.close()
        messagebox.showinfo("Логин изменен", f"Логин пользователя {old_username} изменен на {new_username}.")

    def add_user(self):
        username = tk.simpledialog.askstring("Добавить пользователя", "Введите имя нового пользователя:")
        if not username:
            return

        password = tk.simpledialog.askstring("Добавить пользователя", "Введите пароль для нового пользователя:")
        if not password:
            return

        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Пользователь добавлен", f"Пользователь {username} добавлен.")

    def delete_user(self):
        username = tk.simpledialog.askstring("Удалить пользователя", "Введите имя пользователя для удаления:")
        if not username:
            return

        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Пользователь удален", f"Пользователь {username} удален из базы данных.")

    def unblock_user(self):
        username = tk.simpledialog.askstring("Разблокировать пользователя",
                                             "Введите имя пользователя для разблокировки:")
        if not username:
            return

        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_blocked = 0 WHERE username = ?', (username,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Пользователь разблокирован", f"Пользователь {username} разблокирован.")

    def view_users(self):
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, is_blocked FROM users')
        users_data = cursor.fetchall()
        conn.close()

        if users_data:
            user_list = "\n".join(
                [f"Пользователь: {user[0]}, Пароль: {user[1]}, Заблокирован: {user[2]}" for user in users_data])
            messagebox.showinfo("Список пользователей", user_list)
        else:
            messagebox.showinfo("Список пользователей", "В базе данных нет пользователей.")

    def about_program(self):
        about_info = "Программа для администратора\nАвтор: [Григорий Сухецкий]\nВерсия: 1.0"
        messagebox.showinfo("О программе", about_info)
