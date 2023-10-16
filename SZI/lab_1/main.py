from DatabaseInit import DatabaseInitializer
from LoginForm import LoginForm

if __name__ == '__main__':



    db_initializer = DatabaseInitializer('mydatabase.db')
    db_initializer.initialize_database()

    password_rules = {
        "min_length": 8  # Минимальная длина пароля
    }
    # Здесь введите имя пользователя и его индивидуальные правила для пароля
    username = "ADMIN"
    app = LoginForm(username, password_rules)
    print(app.is_valid_password("1234Br.1!"))
    app.mainloop()
