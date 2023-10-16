import argparse
import base64
import hashlib
import os
from cryptography.fernet import Fernet
import string
import random


def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password) and
                all(password.count(c) <= 1 for c in password)):
            return password


# def convert_key_to_password(key):
#     try:
#         # Декодируем URL-безопасную base64-строку в байты
#         key_bytes = base64.urlsafe_b64decode(key)
#         # Переводим байты обратно в строку
#         password = key_bytes.decode('utf-8')
#         return password
#     except Exception as e:
#         print(f"Ошибка при конвертации ключа в пароль: {e}")
#         return None

def convert_password_to_key(password):
    try:
        # Переводим строку пароля в байты
        hashed_key = hashlib.sha256(password.encode()).digest()
        # Декодируем байты в URL-безопасную base64-строку
        key = base64.urlsafe_b64encode(hashed_key)
        return key
    except Exception as e:
        print(f"Ошибка при конвертации пароля в ключ: {e}")
        return None


def check_password_validity(password):
    if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password)):
        return True
    return False


def encrypt_file(input_file, output_file, password):
    check = False
    if password:
        if not check_password_validity(password):
            print("Ошибка: Неверный формат пароля. Пароль должен соответствовать заданным требованиям.")
            return
        else:
            key = password
            check = True


    else:
        key = Fernet.generate_key()

    if not check:
        print("Ваш пароль ", key.decode())
    if check:
        print("Ваш пароль ", key)
        key = convert_password_to_key(key)
    cipher_suite = Fernet(key)

    with open(input_file, 'rb') as file:
        file_data = file.read()

    encrypted_data = cipher_suite.encrypt(file_data)

    with open(output_file, 'wb') as file:
        file.write(encrypted_data)

    # with open("key.key", "wb") as key_file:
    #     key_file.write(key)


def decrypt_file(input_file, output_file, password):
    if password:

        if not check_password_validity(password):
            print("Ошибка: Неверный формат пароля. Пароль должен соответствовать заданным требованиям.")
            return

        if password[-1] != "=":
            password = convert_password_to_key(password)

        cipher_suite = Fernet(password)

        with open(input_file, 'rb') as file:
            file_data = file.read()

        decrypted_data = cipher_suite.decrypt(file_data)

        with open(output_file, 'wb') as file:
            file.write(decrypted_data)
    else:
        print("Введите пароль")


def main():
    parser = argparse.ArgumentParser(
        description="Шифрование и дешифрование файлов с использованием пользовательского пароля")
    parser.add_argument("input_file", help="Исходный файл")
    parser.add_argument("output_file", help="Файл для сохранения результата")
    parser.add_argument("--password", help="Пароль для шифрования/дешифрования")
    parser.add_argument("--c", action="store_true", help="Зашифровать файл")
    parser.add_argument("--e", action="store_true", help="Расшифровать файл")

    args = parser.parse_args()

    if not args.c and not args.e:
        parser.print_help()
    else:
        if not args.password:
            args.password = input("Введите пароль: ")

        if args.c:
            encrypt_file(args.input_file, args.output_file, args.password)
            print(f"Файл успешно зашифрован с использованием пароля.")
        elif args.e:
            decrypt_file(args.input_file, args.output_file, args.password)
            print(f"Файл успешно расшифрован с использованием пароля.")


if __name__ == "__main__":
    main()
