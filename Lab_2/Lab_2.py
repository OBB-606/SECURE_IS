"""
Программа должна моделировать процессы (на стороне клиента и сервера) регистрации и идентификации/аутентификации пользователя  по протоколу LAMPORT HASH CHAIN.

Схема алгоритма (протокола):
1) клиент и сервер договариваются о числе N, оно может быть несекретно
2) Клиент выбирает случайное большое число P(128 бит)
3) Клиент рекурсивно хеширует это число P N раз
4) Сервер инициализирует счетчик успешных аутентификаций клиента. При инициализации должен быть равным 1

"""
import time
import random
import sys
import json
from random import getrandbits
from hashlib import pbkdf2_hmac

dict_of_user_information:dict = {}

def read_json_file(filename: str):
    global dict_of_user_information
    with open(f'{filename}') as read_file:
        return json.load(read_file)

def write_json_file(filename: str):
    global dict_of_user_information
    with open(f'{filename}', 'w') as write_file:
        json.dump(dict_of_user_information, write_file, indent=3)


def hash_password(password:str, count:int):
    for i in range(count):
        password = pbkdf2_hmac('sha256', password.encode(), ''.encode(), 10000).hex()
    return password


def register():
    global dict_of_user_information
    login_user = login()
    if dict_of_user_information[login_user]['role_in_system'] == 'admin':
        login_new_user = input("<Server to Client> enter login new user: ")
        password_new_user = input("<Server to Client> enter password new user: ")
        count_hash_iteration = int(input("<Server to Client> enter count hash iteration: "))
        role_in_system = input("<Server to Client> enter role new user in system: ")
        dict_of_user_information[login_new_user] = {'password': hash_password(password_new_user, count_hash_iteration), 'count_hash_iteration': count_hash_iteration, 'count_try_true': 1, 'role_in_system':role_in_system}
        write_json_file('db.json')
    else:
        print("<Server to Client> --- недостаточно прав")
        sys.exit()

def wait():
    for i in range(40):
        print("###", end="")
        time.sleep(0.1)
def login():
    global dict_of_user_information
    login = input("<Server to Client> --- Введите логин: ")
    password = input("<Server to Client> --- Введите пароль: ")
    password_hash_in_client_side = hash_password(password, dict_of_user_information[login]['count_hash_iteration'] - dict_of_user_information[login]["count_try_true"])
    print(f"<Server to client> --- количество успешных аутентификаций : {dict_of_user_information[login]['count_try_true']}")
    time.sleep(0.5)
    print(f"<Server to client> --- количество итераций хеширования {dict_of_user_information[login]['count_hash_iteration']}")
    time.sleep(0.5)
    print(f"<Client to Server> --- пароль был захеширован на стороне клиента {dict_of_user_information[login]['count_hash_iteration'] - dict_of_user_information[login]['count_try_true']} раз и передан на сервер")
    time.sleep(0.5)
    print(f"<Server to client> --- На стороне сервера переданный хеш был захеширован {dict_of_user_information[login]['count_try_true']} раз ")
    time.sleep(0.5)
    print(f"<Server to client> --- происходит проверка   ", end="")
    wait()
    print()
    password_hash_in_server_side = hash_password(password_hash_in_client_side, dict_of_user_information[login]['count_try_true'] )

    if password_hash_in_server_side == dict_of_user_information[login]['password']:
        print(f"<Server to client> --- аутентификация завершилась успешно")
        dict_of_user_information[login]['count_try_true'] += 1
        write_json_file('db.json')
        return login
    else:
        print(f"<Server to client> --- аутентификация завершилась не успешно")
        sys.exit()
def __main__():
    global dict_of_user_information
    dict_of_user_information = read_json_file('db.json')
    question_ident = int(input("Регистрация (1)/ авторизация (2): "))
    if question_ident == 1:
        register()
    elif question_ident == 2:
        login()




if __name__ == '__main__':
    __main__()