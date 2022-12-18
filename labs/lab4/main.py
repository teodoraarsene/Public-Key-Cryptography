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

import math
import random

LOWER_BOUND = 23
UPPER_BOUND = 101


class Rabin:
    def __init__(self, private_key: tuple[int, int] = None):
        self.__private_key = private_key if private_key else self.__generate_private_key()
        self.__public_key = self.__compute_public_key()
        self.__len_plaintext_unit, self.__len_ciphertext_unit = self.__compute_lens_message_unit()

    @staticmethod
    def __is_prime(no: int) -> bool:
        """
        Checks if a number is prime
        :param no: the number to be checked
        :return: True if the number is prime, False otherwise
        """
        if no <= 1:
            return False

        for i in range(2, int(no ** (1 / 2)) + 1):
            if no % i == 0:
                return False

        return True

    def __generate_private_key(self) -> tuple[int, int]:
        """
        Generates 2 random large distinct primes of approximately same size
        :return: the tuple containing the 2 primes
        """
        primes = [i for i in range(LOWER_BOUND, UPPER_BOUND + 1) if self.__is_prime(i)]
        p = random.choice(primes)
        q = random.choice(primes)

        while p == q:
            p = random.choice(primes)

        return p, q

    def __compute_public_key(self) -> int:
        """
        Gets the public key based on the public key
        :return: the private key
        """
        return self.__private_key[0] * self.__private_key[1]

    def __compute_lens_message_unit(self) -> tuple[int, int]:
        """
        Calculates the lengths of the text that is processed when encrypting and decrypting
            27^k < n < 27^l, where k is the plain text's length and l is the cipher text's length
        :return: k, l
        """
        # 27^k < n < 27^l
        # k < log27(n) < l
        k = int(math.log(self.__public_key, 27))
        l = k + 1
        while 27 ** l < self.__public_key:
            l += 1

        return k, l

    def __compute_numerical_representation_of_text(self, text: str, encrypt=True) -> list[int]:
        """
        Computes the numerical representation of a text split in k / l sized pieces
        :param text: the input text
        :param encrypt: if True, the length of the plaintext unit is used, otherwise the length of the ciphertext
        :return: a list of the numerical representation for each part of the text
        """
        text = text.lower()
        len_unit = self.__len_plaintext_unit if encrypt else self.__len_ciphertext_unit

        # split the text into k sized parts
        # if the length of the text is not divisible by k, last part will be completed with '_'
        split_text = list()
        for i in range(0, len(text), len_unit):
            split_text.append(text[i: i + len_unit])

        if len(split_text[-1]) is not len_unit:
            split_text[-1] += '_' * (len_unit - len(split_text[-1]))

        # compute the numerical correspondent for each part of the text
        # e.g.: BED → 2 · 27^2 + 5 · 27 + 4 = 1597
        numerical_representation = list()
        for seq in split_text:
            number = 0
            for i in range(len(seq)):
                if seq[i] == '_':
                    correspondent = 0
                else:
                    correspondent = ord(seq[i]) - ord('a') + 1
                number += correspondent * 27 ** (len_unit - i - 1)
            numerical_representation.append(number)

        return numerical_representation

    def __compute_text_from_numerical_presentation(self, numerical_representation: list[int], encrypt=True) -> str:
        """
        Computes and puts together the l sized sequences of text corresponding to the numerical representation
        :param numerical_representation: the numerical representation of text
        :param encrypt: if True, the length of the ciphertext unit is used, otherwise the length of the plaintext
        :return: the corresponding text
        """
        len_unit = self.__len_ciphertext_unit if encrypt else self.__len_plaintext_unit

        text_representation = str()
        for no in numerical_representation:
            for i in range(len_unit):
                coefficient = no // 27 ** (len_unit - i - 1)
                no %= 27 ** (len_unit - i - 1)
                letter = chr(coefficient - 1 + ord('A')) if coefficient else '_'
                text_representation += letter

        return text_representation

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypts the given text using the Rabin public key cryptosystem
        :param plaintext: the text to be encrypted
        :return: the set of all corresponding ciphertexts
        """
        plaintext_numerical_representation = self.__compute_numerical_representation_of_text(plaintext)
        ciphertext_numerical_representation = list()
        for plaintext_numerical_eq in plaintext_numerical_representation:
            cipher_numerical_eq = plaintext_numerical_eq ** 2 % self.__public_key
            ciphertext_numerical_representation.append(cipher_numerical_eq)

        ciphertext = self.__compute_text_from_numerical_presentation(ciphertext_numerical_representation)
        return ciphertext

    @staticmethod
    def __get_modular_square_root(no: int, mod: int) -> int:
        """
        Calculates the modular square of a number
        :param no: the number whose modulus square is calculated
        :param mod: the modulus
        :return: the modular square
        """
        no = no % mod

        for x in range(2, mod):
            if (x * x) % mod == no:
                return x

        return None

    def __extended_euclid(self, a: int, b: int) -> tuple[int, int]:
        """
        Solves the extended euclid equation for a and b
        :param a: the first number
        :param b: the second number
        :return: tuple the found coefficients
        """
        if b == 0:
            return 1, 0

        (x, y) = self.__extended_euclid(b, a % b)
        k = a // b

        return y, x - k * y

    def __chinese_remainder_theorem(self, a1: int, a2: int) -> list[int, int, int, int]:
        """
        Computes the four solutions of the system:
            x = +/-a1 mod p
            x = +/-a2 mod q
        """
        (x, y) = self.__extended_euclid(self.__private_key[0], self.__private_key[1])

        x1 = a2 * x * self.__private_key[0] + a1 * y * self.__private_key[1]
        x2 = -a2 * x * self.__private_key[0] + a1 * y * self.__private_key[1]
        x3 = a2 * x * self.__private_key[0] + -a1 * y * self.__private_key[1]
        x4 = -a2 * x * self.__private_key[0] + -a1 * y * self.__private_key[1]

        x1 = (x1 % self.__public_key + self.__public_key) % self.__public_key
        x2 = (x2 % self.__public_key + self.__public_key) % self.__public_key
        x3 = (x3 % self.__public_key + self.__public_key) % self.__public_key
        x4 = (x4 % self.__public_key + self.__public_key) % self.__public_key

        return [x1, x2, x3, x4]

    def decrypt(self, ciphertext: str) -> list[str]:
        """
        Decrypts the given text using the Rabin public key cryptosystem
        :param ciphertext: the text to be decrypted
        :return: the corresponding plaintext
        """
        ciphertext_numerical_representation = self.__compute_numerical_representation_of_text(ciphertext, False)
        square_root_solutions = list()
        for ciphertext_numerical_eq in ciphertext_numerical_representation:
            solution1 = self.__get_modular_square_root(ciphertext_numerical_eq, self.__private_key[0])
            solution2 = self.__get_modular_square_root(ciphertext_numerical_eq, self.__private_key[1])
            square_root_solutions.append([solution1, solution2])

        system_solutions = list()
        for sol in square_root_solutions:
            all_sols = self.__chinese_remainder_theorem(sol[0], sol[1])
            # eliminate the solutions which are greater than 27^2
            system_solutions.append([sol for sol in all_sols if sol < 27**2])

        ciphertexts = list()
        # associate the units of the solution to construct the possible plaintexts
        for i in range(len(system_solutions[0])):
            solution_pair = list()
            for j in range(len(system_solutions)):
                solution_pair.append(system_solutions[j][i])

            current_ciphertext = self.__compute_text_from_numerical_presentation(solution_pair, False)
            ciphertexts.append(current_ciphertext)

        return ciphertexts


if __name__ == '__main__':
    r = Rabin((31, 53))
    c = r.encrypt('game')
    print(c)
    p = r.decrypt(c)
    print(p)

    print('-------------------')

    c = r.encrypt('hello')
    print(c)
    p = r.decrypt(c)
    print(p)
