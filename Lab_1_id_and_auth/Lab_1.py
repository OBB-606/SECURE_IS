"""
Программа должна моделировать процессы регистрации и идентификации/аутентификации пользователя с salting passwords.
Программа должна демонстрировать значения UserID, пароль, хеш-значение пароля с солью и без, соль и т.д.
на различных этапах регистрации и идентификации/аутентификации.
Пояснить, как salting passwords защищает от атак полного перебора (брутфорс) или атак с помощью предварительно
построенных радужных таблиц?


Задается вопрос: регаться/войти -> соответствующая функция
db.json - username - hash_password - role

"""
import hashlib
import sys
import json

dict_of_user_information:dict = {}

def read_json_file(filename: str):
    global dict_of_user_information
    with open(f'{filename}') as read_file:
        return json.load(read_file)

def write_json_file(filename: str):
    global dict_of_user_information
    with open(f'{filename}', 'w') as write_file:
        json.dump(dict_of_user_information, write_file, indent=3)

def login():
    login = input('Enter login: ')
    password = input('Enter password: ')
    hash = hashlib.pbkdf2_hmac('sha256', password.encode(), dict_of_user_information[login][1].encode(), 100000).hex()
    if dict_of_user_information[login][0] == hash:
        print(f"Вы успешно зашли в систему под логином {login} c ролью {dict_of_user_information[login][1]}")
        return login
    else:
        print('Вы не зашли в систему')
        return None

def register():
    global dict_of_user_information
    login_ = login()
    if dict_of_user_information[login_][1] == 'admin':
        login_new_user = input("enter login new user: ")
        password_new_user = input("enter password new user: ")
        role_new_user = input("enter role new user: ")
        hash = hashlib.pbkdf2_hmac('sha256', password_new_user.encode(), role_new_user.encode(), 100000).hex()
        dict_of_user_information[login_new_user] = [hash, role_new_user]
        write_json_file('db.json')
        print(f"Пользователь {login_new_user} c ролью {role_new_user} успешно зарегистрирован")
    else:
        print(f"У вас недостаточно прав для регистрации нового пользователя, так как ваша роль {dict_of_user_information[login_][1]} ")
        sys.exit()
def __main__():
    global dict_of_user_information
    dict_of_user_information = read_json_file('db.json')
    question_log_auth = int(input("do you want register new user(1) or sign in(2)?"))
    if question_log_auth == 1:
        register()
    elif question_log_auth == 2:
        login()
    else:
        print("Wrong input data! Bye")
        sys.exit()


if __name__ == '__main__':
    __main__()


