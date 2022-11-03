"""
the hill cipher (m = 2)
    P = C = (Zn)^2
    K = {k belongs to M2(Zn) | k is invertible and gcd(det(k), n) = 1}
    for any k in K, for any x, y in (Zn)^2:
            ek(x) = x*k mod n
            dk(y) = y*k^(-1) mod n
        ek:P -> C and dk:C -> P such that
            dk(ek(x)) = x for every x in P
    ek is injective <=> gcd(det(k), n) = 1
 """
import random


def get_input_matrix(plaintext: str) -> list[list]:
    """
    Computes the matrix with 2 columns corresponding to the plaintext to be encrypted.
    If the plaintext's length is odd, an extra random number will be added to complete the matrix
    [_ a b c d e f g h i j  k  l  m  n  o  p  q  r  s  t  u  v  w  x  y  z ]
    [0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26]

    ex: plaintext = 'four'
        numerical = [[6, 15], [21, 18]]
    """
    plaintext = plaintext.lower()
    numerical = [[]]
    for i in range(len(plaintext)):
        if i % 2:
            numerical[i // 2].append(ord(plaintext[i]) - ord('a') + 1)
            numerical.append([])
        else:
            numerical[i // 2] = [ord(plaintext[i]) - ord('a') + 1]

    if not numerical[-1]:
        numerical.pop()
    else:
        numerical[-1].append(random.randint(0, 26))

    return numerical


def get_output_string(encrypted_matrix: list[list]) -> str:
    """
    Computes the encrypted string corresponding to the encryption matrix
    [0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26]
    [_ A B C D E F G H I J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z ]
   """
    text = str()
    for i in range(len(encrypted_matrix)):
        for j in range(2):
            text += chr(encrypted_matrix[i][j] - 1 + ord('A'))
    return text


def generate_key_matrix(n) -> list[list]:
    """
    Generates a random key matrix with elements from Zn, further used in the encryption process
    """
    key_matrix = list()
    for i in range(2):
        key_matrix.append([])
        for j in range(2):
            key_matrix[i].append(random.randint(0, n - 1))

    return key_matrix


def multiply(vector: list, matrix: list[list]) -> list:
    """
    Performs the multiplication between a horizontal vector (M(1*2)) and a matrix (M(2*2)), whose result is a
    horizontal vector (M(1*2))
        -> vector = [x, y]
        -> matrix = [ [a, b],
                      [c, d] ]
        -> result = [x*a + y*c, x*b + y*d]
    """
    result = [0, 0]
    for i in range(2):
        for j in range(2):
            result[j] += vector[i] * matrix[i][j]

    return result


def hill_cipher2(plaintext: str, key_matrix: list[list] = None, n: int = 27) -> str:
    """
    Algorithm's steps:
        1. Transform the input text into a matrix with 2 columns
        2. Compute the encryption matrix by multiplying each row in the matrix resulted from Step 1 with the key matrix
        3. Transform the matrix obtained from Step 2 to ciphertext
    """
    input_matrix = get_input_matrix(plaintext)
    if not key_matrix:
        key_matrix = generate_key_matrix(n)

    # encryption step
    encryption_matrix = list()
    for i in range(len(input_matrix)):
        encryption_matrix.append(multiply(input_matrix[i], key_matrix))

    # modulo n step
    for i in range(len(encryption_matrix)):
        for j in range(2):
            encryption_matrix[i][j] %= n

    ciphertext = get_output_string(encryption_matrix)

    return ciphertext


def get_matrix_determinant(matrix: list[list]) -> int:
    """
    Computes the determinant of a 2x2 matrix.
        K = [ [a, b],
              [c, d] ]
        det(K) = a*d - c*b
        K^(-1) = 1/(a*d - b*c) * [ [d, -b]
                                   [-c, a] ]
    """
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def gcd_extended(a: int, b: int) -> tuple[int, int, int]:
    # base case
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = gcd_extended(b % a, a)

    # update x and y using results of the recursive call
    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


def get_adjoint_matrix(matrix: list[list]) -> list[list]:
    """
    Computes the adjoint matrix of a 2x2 matrix.
        K = [ [a, b],
              [c, d] ]
        A = [ [d, -b],
              [-c, a] ]
    """
    return [[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]]


def get_modular_inverse(matrix: list[list], n: int) -> list[list]:
    """
    Computes the modular inverse of a 2x2 matrix.
        K = [ [a, b],
              [c, d] ]
        det(K) = a*d - c*b
        K^(-1) % n = det(K)^(-1) % n * [ [d, -b]   % n
                                   [-c, a] ]
       the problem of det(K)^(-1) % n is solved by using the extended euclidean algorithm
       to find the modular multiplicative inverse of the matrix determinant
    """

    det = get_matrix_determinant(matrix)
    if not det:
        raise Exception('det of key matrix is 0')

    det %= n
    _, modular_multiplicative_inverse, _ = gcd_extended(det, n)
    while modular_multiplicative_inverse < 0:
        modular_multiplicative_inverse += n

    # modulo n the matrix of cofactors
    adjoint_matrix = get_adjoint_matrix(matrix)
    for i in range(2):
        for j in range(2):
            while adjoint_matrix[i][j] < 0:
                adjoint_matrix[i][j] += n

    # multiplication between the modular_multiplicative_inverse and the adjoint matrix modulo n
    for i in range(2):
        for j in range(2):
            adjoint_matrix[i][j] *= modular_multiplicative_inverse
            adjoint_matrix[i][j] %= n

    return adjoint_matrix


if __name__ == '__main__':
    text = 'four'
    key = [[11, 8], [3, 7]]
    n = 27
    print(f'[HILL CIPHER]\n[ENCRYPTION]\n\tPLAINTEXT: {text}\n\tKEY MATRIX: {key}\n\tN: {n}')
    cipher = hill_cipher2(plaintext=text, key_matrix=key, n=n)
    print(f'\tCIPHERTEXT: {cipher}')

    key_inv = get_modular_inverse(key, n)
    print(f'[DECRYPTION]\n\tCIPHERTEXT: {cipher}\n\tINVERSE OF KEY MATRIX: {key_inv}\n\tN: {n}')
    text_decrypted = hill_cipher2(plaintext=cipher, key_matrix=key_inv, n=n).lower()
    print(f'\tCIPHERTEXT: {text_decrypted}')
