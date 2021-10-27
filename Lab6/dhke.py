# 50.042 FCS Lab 6 template
# Year 2021

import primes
import random


def dhke_setup(nb):
    # choose a large prime number
    p = primes.gen_prime_nbits(nb)
    a = random.randint(2, p - 2)

    return p, a


def gen_priv_key(p):
    return random.randint(2, p - 2)


def get_pub_key(alpha, a, p):
    return primes.square_multiply(alpha, a, p)


def get_shared_key(keypub, keypriv, p):
    return primes.square_multiply(keypub, keypriv, p)


if __name__ == "__main__":
    p, alpha = dhke_setup(80)
    print("Generate P and alpha:")
    print("P:", p)
    print("alpha:", alpha)
    print()
    a = gen_priv_key(p)
    b = gen_priv_key(p)
    print("My private key is: ", a)
    print("Test other private key is: ", b)
    print()
    A = get_pub_key(alpha, a, p)
    B = get_pub_key(alpha, b, p)
    print("My public key is: ", A)
    print("Test other public key is: ", B)
    print()
    sharedKeyA = get_shared_key(B, a, p)
    sharedKeyB = get_shared_key(A, b, p)
    print("My shared key is: ", sharedKeyA)
    print("Test other shared key is: ", sharedKeyB)
    print("Length of key is %d bits." % sharedKeyA.bit_length())
