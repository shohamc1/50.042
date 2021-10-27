# 50.042 FCS Lab 6 template
# Year 2021

import random


def square_multiply(a: int, x: int, n: int) -> int:
    res = 1

    for i in bin(x)[2:]:
        res = pow(res, 2) % n
        if i == "1":
            res = res * a % n

    return res


def miller_rabin(n: int, a: int) -> bool:
    # n -> number
    # a -> number of iterations to check
    # implementation from pseudocode found in Wikipedia (https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Miller%E2%80%93Rabin_test)

    r = 0
    d = n - 1

    while d % 2 == 0:
        d = d // 2
        r += 1

    for i in range(a):
        rand_int = random.randint(2, n - 2)
        x = square_multiply(rand_int, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2) % n

            if x == n - 1:
                break

        else:
            return False

    return True


def gen_prime_nbits(n: int) -> int:
    x = random.getrandbits(n)

    while not miller_rabin(x, 2):
        x = random.getrandbits(n)

    return x


if __name__ == "__main__":
    print("Is 561 a prime?")
    print(miller_rabin(561, 2))
    print("Is 27 a prime?")
    print(miller_rabin(27, 2))
    print("Is 61 a prime?")
    print(miller_rabin(61, 2))

    print("Random number (100 bits):")
    print(gen_prime_nbits(100))
    print("Random number (80 bits):")
    print(gen_prime_nbits(80))
