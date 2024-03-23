import random
from sympy import nextprime


def gcd(a, b):
    # Функция gcd(a, b) вычисляет наибольший общий делитель двух чисел a и b.
    while b:
        # Запускаем цикл, пока b не равно 0.
        # В Python 0 интерпретируется как False, а любое ненулевое число как True.
        a, b = b, a % b
        # Обновляем значения переменных a и b:
        # Новое значение a становится равным b,
        # а новое значение b становится остатком от деления a на b.
    return a
    # Как только b становится равным 0, возвращаем a, которая содержит НОД двух чисел.


# генерация рандомных чисел по правилу для частотного теста
def gen_right_prime_number(start, end):
    x = nextprime(random.randint(0xfffffff, 0xffffffffffffff))
    while x % 4 != 3:
        x = nextprime(random.randint(0xfffffff, 0xffffffffffffff))
    return x


def create_rand_num(m):
    # 1 step
    # генерируем p и q (случайные, секретные, большие и различные)
    q = gen_right_prime_number(0xfffffff, 0xffffffffffffff)
    p = gen_right_prime_number(0xffffffff, 0xffffffffffffff)
    # если числа одинаковые, то генерируем до тех пор, пока не станут разными
    while p == q:
        q = gen_right_prime_number(0xfffffff, 0xffffffffffffff)
        p = gen_right_prime_number(0xffffffff, 0xffffffffffffff)
    print(p)
    print(q)
    N = p * q
    print("N = ", N)
    # 2 step
    s = N
    while gcd(N, s) > 1:
        s = random.randint(1, N)
    print(gcd(N, s), s)
    u = [(s * s) % N]
    print(u)
    #step 3
    x = []
    for i in range(0, m):
        u.append(u[i]**2 % N)
        x.append(u[i+1] & 0b1)
    #step 4
    print(x.count(0), x.count(1))
    print("Test 1 = ", frequency_test(x))
    print("Test 2 = ", same_bits_test(x))
    print("Test 3 = ", deviations_test(x))
    return x


# Функция, которая преобразовывает последовательность в -1 и 1 в частотном тесте
def preprocessing_list(x):
    y = []
    for elem in x:
        y.append(elem * 2 - 1)
    return y


# Частотный тест
def frequency_test(epsilon):
    output = open("TestFile.txt", "a")
    output.write("=== frequency test ===\n")
    # output.write("start list = {0}\n".format(epsilon))
    X = preprocessing_list(epsilon)
    # output.write("preprocessing list = {0}\n".format(X))
    Sn = 0
    for elem in X:
        Sn += elem
    # Вычисляем статистику по формуле
    S = abs(Sn) / len(X) ** 0.5
    # выводим результат теста
    output.write("S = {0}\n".format(S))
    output.write("Result = {0}\n".format(S <= 1.82138636))
    output.write("=== end test ===\n\n")
    output.close()

    return S <= 1.82138636


# Тест на последовательность одинаковых бит
def same_bits_test(epsilon):
    output = open("TestFile.txt", "a")
    output.write("=== same bits test ===\n")
    # output.write("start list = {0}\n".format(epsilon))
    pi = 0
    n = len(epsilon)
    output.write("n = {0}\n".format(n))
    # вычисляем частоту встречаемости единиц в последовательности
    for elem in epsilon:
        pi += elem
    pi = pi / n
    output.write("pi = {0}\n".format(pi))
    V = 1
    # вычисляем значение V по формуле из методички
    for i in range(1, n):
        V += int(epsilon[i] == epsilon[i-1])
    output.write("V = {0}\n".format(V))
    # вычисляем статистику
    S = abs(V - 2 * n * pi * (1 - pi)) / (2 * (2 * n) ** 0.5 * pi * (1 - pi))
    # выводим результат теста
    output.write("S = {0}\n".format(S))
    output.write("Result = {0}\n".format(S <= 1.82138636))
    output.write("=== end test ===\n\n")
    output.close()

    return S <= 1.82138636


# Расширенный тест на произвольные отклонения
def deviations_test(epsilon):
    output = open("TestFile.txt", "a")
    output.write("=== deviations test ===\n")
    # output.write("start list = {0}\n".format(epsilon))
    # преобразовываем последовательность в -1 и 1
    X = preprocessing_list(epsilon)
    # output.write("preprocessing list = {0}\n".format(X))
    S = [X[0]]
    # вычисляем суммы S(i) последовательно удлиняющейся последовательности
    for i in range(1, len(epsilon)):
        S.append(S[i-1] + X[i])
    # output.write("S = {0}\n".format(S))
    Sn = [0]
    # формируем новую последовательность Sn
    for elem in S:
        Sn.append(elem)
    Sn.append(0)
    # output.write("Sn = {0}\n".format(Sn))
    # вычисляем L - количество нулей в последовательности Sn
    L = -1
    for elem in Sn:
        L += int(elem == 0)
    output.write("L = {0}\n".format(L))
    # Для каждого из 18 состояний вычисляется ksi(j), которое показывает, сколько раз состояние j
    # встречалось в последовательности Sn.
    ksi = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for elem in Sn:
        if (elem >= -9) and (elem < 0):
            ksi[elem + 9] += 1
        if (elem > 0) and (elem <= 9):
            ksi[elem + 8] += 1
    Y = []
    output.write("ksi = {0}\n".format(ksi))
    # Вычисляем 18 статистик Y(j) для каждого состояния j
    for j in range(-9, 0):
        Y.append(abs(ksi[j + 9] - L) / (2 * L * (4 * abs(j) - 2)) ** 0.5)
    for j in range(1, 10):
        Y.append(abs(ksi[j + 8] - L) / (2 * L * (4 * abs(j) - 2)) ** 0.5)
    output.write("Y = {0}\n".format(Y))

    # выводим результат теста
    result = True
    for elem in Y:
        result = result and (elem <= 1.82138636)
    output.write("Result list = {0}\n".format(result))
    output.write("=== end test ===\n\n")
    output.close()
    return result


