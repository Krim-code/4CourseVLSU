import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


class UserWindow(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title("Пользователь")
        self.geometry("400x200")

        self.label = tk.Label(self, text=f"Добро пожаловать, {username}!")
        self.label.pack()

        self.change_password_button = tk.Button(self, text="Изменить пароль", command=self.change_password)

        self.change_password_button.pack()

    def change_username(self):
        old_username = tk.simpledialog.askstring("Изменить логин", "Введите текущий логин:")
        if not old_username:
            return

        new_username = tk.simpledialog.askstring("Изменить логин", "Введите новый логин:")
        if not new_username:
            return

        # Проверка старого пароля перед изменением логина
        old_password = tk.simpledialog.askstring("Изменить логин", "Введите старый пароль:")
        if not old_password:
            return

        if self.check_password(old_username, old_password):
            conn = sqlite3.connect('mydatabase.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, old_username))
            conn.commit()
            conn.close()
            messagebox.showinfo("Логин изменен", f"Логин пользователя {old_username} изменен на {new_username}.")
        else:
            messagebox.showerror("Ошибка", "Неверный старый пароль.")

    def change_password(self):

        # Проверка старого пароля перед изменением пароля
        old_password = tk.simpledialog.askstring("Изменить пароль", "Введите старый пароль:")
        if not old_password:
            return

        if self.check_password(self.username, old_password):
            new_password = tk.simpledialog.askstring("Изменить пароль", "Введите новый пароль:")
            if not new_password:
                return

            conn = sqlite3.connect('mydatabase.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, self.username))
            conn.commit()
            conn.close()
            messagebox.showinfo("Пароль изменен", f"Пароль пользователя {self.username} изменен.")
        else:
            messagebox.showerror("Ошибка", "Неверный старый пароль.")

    def check_password(self, username, password):
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, password FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            stored_password = user_data[1]
            if stored_password == password:
                return True
        return False


