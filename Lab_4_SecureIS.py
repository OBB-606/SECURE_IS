"""
Steps Protocol

1) Alice -> A,B,Ra -> Trent
2) Trent -> (Ra, B, K, (K,A)Kb)Ka -> Alice
3) Alice -> (K,A)Kb -> Bob
4) Bob -> (Rb)K -> Alice
5) Alice -> (Rb - 1)K -> Bob
"""

from random import randint as get_random_digit
import pickle
from colorama import Fore, Style
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode


def AES_encrypt(key, iv, plaintext_list):
    """
    Функция для шифрования списка с помощью AES.

    :param key: ключ шифрования
    :param iv: вектор инициализации
    :param plaintext_list: список, который нужно зашифровать
    :return: зашифрованный список в формате base64-encoded строка
    """
    plaintext_str = pickle.dumps(plaintext_list)  # сериализуем список в строку
    # plaintext_bytes = plaintext_str.encode("utf-8")  # переводим строку в байты
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext_bytes = cipher.encrypt(pad(plaintext_str, AES.block_size))  # шифруем и добавляем padding
    ciphertext_b64 = b64encode(ciphertext_bytes).decode("utf-8")  # переводим байты в base64-encoded строку
    return ciphertext_b64


def AES_decrypt(key, iv, ciphertext_b64):
    """
    Функция для дешифрования списка, зашифрованного с помощью AES.

    :param key: ключ шифрования
    :param iv: вектор инициализации
    :param ciphertext_b64: зашифрованный список в формате base64-encoded строки
    :return: дешифрованный список
    """
    ciphertext_bytes = b64decode(ciphertext_b64)  # переводим base64-encoded строку в байты
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_bytes = unpad(cipher.decrypt(ciphertext_bytes), AES.block_size)  # дешифруем и удаляем padding
    # plaintext_str = plaintext_bytes.decode("utf-8")  # переводим байты в строку
    plaintext_list = pickle.loads(plaintext_bytes)  # десериализуем строку в список
    return plaintext_list


def channel_connection(source: str, target: str, object):
    print(f"{Fore.RED}{source}{Style.RESET_ALL} --> {Fore.BLUE}{target}{Style.RESET_ALL} : {Fore.GREEN}{object}{Style.RESET_ALL}")


inicialize_vector = b"this is an IV456"
Alice = 'Alice'
Bob = 'Bob'
Trent = 'Trent'
Ra = get_random_digit(0, 999)
Rb = get_random_digit(0, 999)
print("""
1) Alice -> A,B,Ra -> Trent
2) Trent -> (Ra, B, K, (K,A)Kb)Ka -> Alice
3) Alice -> (K,A)Kb -> Bob
4) Bob -> (Rb)K -> Alice
5) Alice -> (Rb - 1)K -> Bob

A - Alice 
B - Bob
Ra - Случайное число Алисы
Rb - Случайное число Боба
Ka - Ключ Алисы
Kb - Ключ Боба
K - Сессионный Ключ
""")


print(f"Alice and Bob generated random digit: {Ra} and {Rb}")

# Step 1
print("1) Alice -> A,B,Ra -> Trent")
current_message = [Alice, Bob, Ra]
channel_connection(Alice, Trent, Ra)
# print(f"Alice ---> Trent: Alice, Bob, {Ra}")
with open('alice_key.txt', 'r') as read_file:
    alice_key = read_file.read().encode()
with open('bob_key.txt', 'r') as read_file:
    bob_key = read_file.read().encode()
session_key = b"ThisIsSessionKey"

# Step 2
print("2) Trent -> (Ra, B, K, (K,A)Kb)Ka -> Alice")
current_message = AES_encrypt(alice_key, inicialize_vector, [Ra, Bob, session_key, AES_encrypt(bob_key, inicialize_vector, [session_key, Alice])])
channel_connection(Trent, Alice, current_message)

# Step 3
print("3) Alice -> (K,A)Kb -> Bob")
current_message = AES_encrypt(bob_key, inicialize_vector, [session_key, Alice])
channel_connection(Alice, Bob, current_message)

# Step 4
print("4) Bob -> (Rb)K -> Alice")
current_message = AES_encrypt(session_key, inicialize_vector, Rb)
channel_connection(Bob, Alice, current_message)

# Step 5
print("5) Alice -> (Rb - 1)K -> Bob")
current_message = AES_encrypt(session_key, inicialize_vector, Rb-1)
channel_connection(Alice, Bob, current_message)

# Connection installed
print("После установления соединения: ")
print("В закрытом виде: ")
# To Bob
current_message = AES_encrypt(session_key, inicialize_vector, "Hello, Bob!")
channel_connection(Alice, Bob, current_message)
print("В открытом виде: ")
channel_connection(Alice, Bob, AES_decrypt(session_key, inicialize_vector, current_message))

# To Alice
print("В закрытом виде: ")
current_message = AES_encrypt(session_key, inicialize_vector, "Hello, Alice!")
channel_connection(Bob, Alice, current_message)
print("В открытом виде: ")
channel_connection(Bob, Alice, AES_decrypt(session_key, inicialize_vector, current_message))
print()
