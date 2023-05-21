import random
from sympy import isprime
p = 0
def generate_p():
    global p
    while True:
        tmp = random.randint(999, 99999)
        result = isprime(tmp)
        print(result)
        if result:
            p = tmp
            break
generate_p()
# Параметры протокола
# p = 96529
# p = generate_p()
# g = 5
a = random.randint(1, p-2)  # Случайное число для Alice
b = random.randint(1, p-2)  # Случайное число для Bob
#
def generate_g(p: int):
    q = 3
    for i in range(5, p-1):
        if (p-1)%i == 0 and isprime(i):
            q = i
    g = 0
    # print(q)
    stepen = ((p-1)/q)%p
    for i in range(1, p-1):
        if pow(i, stepen) != 1:
            g = i
    return g

# print(generating_g(p))
g = generate_g(p)
# Шаг 1: Alice отправляет Bob число R1 = g^a mod p
R1 = pow(g, a, p)
print("Alice отправляет Bob число R1 =", R1)

# Шаг 2: Bob отправляет Alice число R2 = g^b mod p
R2 = pow(g, b, p)
print("Bob отправляет Alice число R2 =", R2)

# Шаг 3: Alice вычисляет общий секрет Z = R2^a mod p
Z1 = pow(R2, a, p)
print("Alice вычисляет общий секрет Z =", Z1)

# Шаг 4: Bob вычисляет общий секрет Z = R1^b mod p
Z2 = pow(R1, b, p)
print("Bob вычисляет общий секрет Z =", Z2)

# Проверка: оба значения Z должны быть одинаковы
if Z1 == Z2:
    print("Протокол завершен успешно. Общий секрет Z =", Z1)
else:
    print("Ошибка: значения Z не совпадают.")
