import sqlite3
import tkinter as tk
from tkinter import messagebox
from OpenSSL import crypto
import os

from AdminWindow import AdminWindow
from UserWindow import UserWindow


class LoginForm(tk.Tk):
    def __init__(self, username, password_rules):
        super().__init__()

        self.username = username
        self.password_rules = password_rules

        self.title("Вход")
        self.geometry("300x200")

        self.label_username = tk.Label(self, text="Имя пользователя:")
        self.label_password = tk.Label(self, text="Пароль:")
        self.label_use_certificate = tk.Label(self, text="Использовать сертификат:")

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="•")
        self.use_certificate_var = tk.BooleanVar()
        self.use_certificate_checkbox = tk.Checkbutton(self, variable=self.use_certificate_var)

        self.login_button = tk.Button(self, text="Войти", command=self.login)

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.label_use_certificate.pack()
        self.use_certificate_checkbox.pack()
        self.login_button.pack()

    def login(self):
        entered_username = self.entry_username.get()
        entered_password = self.entry_password.get()
        use_certificate = self.use_certificate_var.get()

        if use_certificate:
            # Проверка сертификата
            self.check_certificate()
        else:
            if self.is_valid_password(entered_password):
                user_data = self.check_user_credentials(entered_username, entered_password)
                if user_data:
                    if user_data['is_admin']:
                        admin_app = AdminWindow()
                        self.destroy()
                    else:
                        user_app = UserWindow(user_data['username'])
                        self.destroy()
                else:
                    messagebox.showerror("Ошибка входа", "Неверное имя пользователя или пароль.")
            else:
                messagebox.showerror("Ошибка входа", "Неверное имя пользователя или пароль.")

    def is_valid_password(self, password):
        if len(password) < self.password_rules["min_length"]:
            return False
        if not any(c.islower() for c in password) or not any(c.isupper() for c in password):
            return False
        if not any(c.isdigit() or c in "!@#$%^&*()_+" for c in password):
            return False
        return True

    def check_user_credentials(self, username, password):
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, is_blocked FROM users WHERE username = ? AND password = ?',
                       (username, password))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            if user_data[2] == 0:
                if username == "ADMIN":
                    return {'username': user_data[0], 'is_admin': True}
                else:
                    return {'username': user_data[0], 'is_admin': False}

        return None

    def check_certificate(self):
        usb_drive = self.find_usb_drive()  # Найти подключенный USB-носитель

        if usb_drive:
            certificate_path = os.path.join(usb_drive, "certificate.crt")

            if os.path.exists(certificate_path):
                with open(certificate_path, 'rb') as cert_file:
                    cert_data = cert_file.read()
                    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)

                    username = cert.get_subject().CN  # Получаем имя пользователя (логин) из сертификата

                    if self.is_valid_username(username):
                        user_data = self.check_user_credentials_for_certithicate(username,
                                                                                 None)  # Пароль передается как None
                        if user_data:
                            if user_data['is_admin']:
                                admin_app = AdminWindow()
                                self.destroy()
                            else:
                                user_app = UserWindow(user_data['username'])
                                self.destroy()
                        else:
                            messagebox.showerror("Ошибка входа", "Неверный логин или пароль.")
                    else:
                        messagebox.showerror("Ошибка входа", "Неверное имя пользователя в сертификате.")

            else:
                return None

        else:
            return None

    def is_valid_username(self, username):
        return True

    def find_usb_drive(self):
        # Поиск подключенных USB-носителей и проверка наличия сертификата
        # Возвращаем путь к USB-носителю или None, если не найдено
        for drive in range(65, 91):  # A: - Z:
            drive_letter = f"{chr(drive)}:"
            drive_path = f"{drive_letter}\\"
            if os.path.exists(drive_path) and os.path.ismount(drive_path):
                if os.path.exists(os.path.join(drive_path, "user_certificate.crt")):
                    return drive_path
        return None

    def check_user_credentials_for_certithicate(self, username, password):
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, is_blocked FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            if user_data[2] == 0:
                if username == "ADMIN":
                    return {'username': user_data[0], 'is_admin': True}
                else:
                    return {'username': user_data[0], 'is_admin': False}

        return None
