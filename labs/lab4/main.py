"""
The Rabin Public Key Cryptosystem
    -> key generation:
        - private key: (p, q) where p, q are 2 random large distinct primes of approximately same size
        - public key: n = p * q
    -> encryption:
        - message: m, where 0 < m < n - 1
        - cypher text: c = m^2 mod n
    -> decryption:
        - with the private key (p, q) determine the 4 square roots m1, m2, m3, m4 of c mod n
        - decide which message, m1, m2, m3 or m4, is the correct one

    P = C = K = Zn
    encryption function: f:Zn -> Zn, f(m) = m^2 mod n
    decryption function: f^(-1):Zn -> Zn, f^(-1)(c) = m1 or m2 or m3 or m4 (square roots of c modulo n)
"""
import random

LOWER_BOUND = 23
UPPER_BOUND = 101
ALPHABET = ['_', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def is_prime(no: int) -> bool:
    """
    Checks if a number is prime
    :param no: the number to be checked
    :return: True if the number is prime, False otherwise
    """
    if no <= 1:
        return False

    for i in range(2, int(no ** (1/2)) + 1):
        if no % i == 0:
            return False

    return True


def generate_private_key() -> tuple[int, int]:
    """
    Generates 2 random large distinct primes of approximately same size
    :return: the tuple containing the 2 primes
    """
    primes = [i for i in range(LOWER_BOUND, UPPER_BOUND + 1) if is_prime(i)]
    p = random.choice(primes)
    q = random.choice(primes)

    while p == q:
        p = random.choice(primes)

    return p, q


def get_public_key(p: int, q: int) -> int:
    """
    Gets the public key based on the public key
    :param p: the first component of the public key
    :param q: the second component of the public key
    :return: the private key
    """
    return p * q


def get_text_processing_len(n: int) -> tuple[int, int]:
    """
    Calculates the lengths of the text that is processed when encrypting and decrypting
        27^k < n < 27^l, where k is the plain text's length and l is the cypher text's length
    :param n: the public key
    :return: k, l
    """
    pass


def get_numerical_representation_of_text(text: str) -> list[int]:
    pass


if __name__ == '__main__':
    print(generate_private_key())
    # print(is_prime(101))
