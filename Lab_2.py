"""
Программа должна моделировать процессы (на стороне клиента и сервера) регистрации и идентификации/аутентификации пользователя  по протоколу LAMPORT HASH CHAIN.

Схема алгоритма (протокола):
1) клиент и сервер договариваются о числе N, оно может быть несекретно
2) Клиент выбирает случайное большое число P(128 бит)
3) Клиент рекурсивно хеширует это число N раз
4) Сервер инициализирует счетчик успешных аутентификаций клиента. При инициализации должен быть равным одному

"""
import random

# print(len('340282366920938463463374607431768211455'))
from random import getrandbits
from hashlib import pbkdf2_hmac
# n = random.randint(300, 10000)
n = 567
# p = getrandbits(128)
p = str(91558193244860674981394116015844070102)

def hash_password(password:str):
    return pbkdf2_hmac('sha256', password.encode(), ''.encode(), 1).hex()

for i in range (1):
    # print(i)
    p = pbkdf2_hmac('sha256', "649b391727342ad2cc9a05152118d90d95b3629d86f4901b5d20baecfcfc99e3".encode(), ''.encode(), 10000).hex()

# 3c2c1a6dd130ff3b3e92b239aa46adb84ad1a64c78f61bd665fefde0b9bbef0f
# 649b391727342ad2cc9a05152118d90d95b3629d86f4901b5d20baecfcfc99e3
print(p)
